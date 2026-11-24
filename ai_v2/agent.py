"""Stage 5: verification agent, with typed READ-ONLY tools.

It only runs on declarations that have findings that could block (or serious ones): its job is
to CONFIRM or REFUTE each finding by going back to the sources (zoom on the label, reference
data, article recomputation, calculation) before an automatic decision is taken. The number of
turns is bounded. No free SQL: only typed tools.

The agent is not trusted blindly either: a "confirmed" verdict is downgraded to "uncertain"
unless it is itself supported (see _confirmation_supported).

Tool names, tool descriptions and tool results are in French: they are model input, like the
prompt (prompts/agent_verify.md).
"""

from __future__ import annotations

import ast
import json
import operator

import numpy as np
from rapidfuzz import fuzz

from .article import CompItem, CompSubstance, composition_from_declaration, compute_article
from .config import Settings, prompt_text
from .db import fetchall
from .declarations import DeclarationDTO
from .documents import LabelDocument
from .extract import MergedLabel
from .llm import LLMClient
from .refdata import KIND_FR, RefData
from .resolve import STATUS_FR, Resolver
from .schemas import AgentOutput, Finding, Severity
from .text import normalise, quote_in_text
from .units import convert

# Zones the agent can zoom on with `voir_page`: (x0, y0, x1, y1) as fractions of the page.
ZONES = {
    "haut": (0, 0, 1, 0.5), "bas": (0, 0.5, 1, 1), "gauche": (0, 0, 0.5, 1), "droite": (0.5, 0, 1, 1),
    "centre": (0.2, 0.2, 0.8, 0.8), "haut-gauche": (0, 0, 0.55, 0.55), "haut-droite": (0.45, 0, 1, 0.55),
    "bas-gauche": (0, 0.45, 0.55, 1), "bas-droite": (0.45, 0.45, 1, 1), "tout": None,
}  # fmt: skip

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_calc(expr: str) -> float:
    """Safe calculator for the agent: walks the AST and only allows numbers and arithmetic
    operators (no names, calls or attributes, so no arbitrary code execution)."""

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError("expression non autorisée")  # returned to the agent as a tool result

    return ev(ast.parse(expr.replace(",", "."), mode="eval"))


def _fn(name: str, description: str, properties: dict, required: list[str]) -> dict:
    """Function-calling tool spec in the Mistral (OpenAI-compatible) format."""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {"type": "object", "properties": properties, "required": required},
        },
    }


# The agent's tools. All of them are read-only. The last one, `rendre_verdict`, ends the loop.
TOOLS = [
    # look at a page image (whole, zoomed on a zone, rotated)
    _fn(
        "voir_page",
        "Affiche l'image d'une page d'étiquette, entière ou zoomée sur une zone, éventuellement tournée "
        "(texte imprimé de travers ou à l'envers), pour lire les petits caractères.",
        {
            "fichier": {"type": "integer"},
            "page": {"type": "integer"},
            "zone": {"type": "string", "enum": list(ZONES)},
            "rotation": {"type": "integer", "enum": [0, 90, 180, 270]},
        },
        ["fichier", "page"],
    ),
    # OCR text of a page (+ rotated OCR text)
    _fn(
        "transcription",
        "Renvoie la transcription OCR d'une page d'étiquette.",
        {"fichier": {"type": "integer"}, "page": {"type": "integer"}},
        ["fichier", "page"],
    ),
    # search the reference data (fuzzy + semantic), returns uids
    _fn(
        "rechercher_referentiel",
        "Cherche un ingrédient/plante/substance dans le référentiel Compl'Alim (renvoie des uid).",
        {"texte": {"type": "string"}},
        ["texte"],
    ),
    # details of one element: status, max doses, mandatory warnings, substances
    _fn(
        "fiche_element",
        "Détail d'un élément du référentiel : statut, risque, doses max par population, avertissements, substances.",
        {"uid": {"type": "string"}},
        ["uid"],
    ),
    # recompute the article with extra elements / quantities
    _fn(
        "calculer_article",
        "Recalcule l'article réglementaire si l'on ajoute des éléments et/ou des quantités de substances à la composition déclarée.",
        {
            "ajouter_uids": {"type": "array", "items": {"type": "string"}},
            "quantites": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"uid": {"type": "string"}, "quantite": {"type": "number"}},
                    "required": ["uid", "quantite"],
                },
            },
        },
        [],
    ),
    # safe arithmetic
    _fn(
        "calculer",
        "Calculatrice (expression arithmétique, ex. '500*0.95*2').",
        {"expression": {"type": "string"}},
        ["expression"],
    ),
    # unit conversion
    _fn(
        "convertir",
        "Convertit une quantité (mg, µg, g, UI, ml…).",
        {
            "valeur": {"type": "number"},
            "de": {"type": "string"},
            "vers": {"type": "string"},
            "substance": {"type": "string"},
        },
        ["valeur", "de", "vers"],
    ),
    # RAG over instructor comments on similar cases
    _fn(
        "doctrine_instructeurs",
        "Exemples de commentaires d'instructeurs sur des cas similaires (doctrine).",
        {"question": {"type": "string"}},
        ["question"],
    ),
    # final answer: one verdict per finding
    _fn(
        "rendre_verdict",
        "Termine la vérification : un verdict par constat.",
        {
            "verdicts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "finding_id": {"type": "string"},
                        "verdict": {"type": "string", "enum": ["confirmed", "refuted", "uncertain"]},
                        "confidence": {"type": "number"},
                        "quote": {"type": "string"},
                        "page": {"type": "integer"},
                        "explanation": {"type": "string"},
                    },
                    "required": ["finding_id", "verdict", "confidence", "explanation"],
                },
            },
            "new_findings": {"type": "array", "items": {"type": "string"}},
        },
        ["verdicts"],
    ),
]


class Doctrine:
    """RAG over instructor comments, so the agent can see how similar cases were handled.

    The declarations of the evaluation set are excluded (`exclude_declarations`): the agent must
    never see the instructor's comment on the very case it is being evaluated on.
    """

    def __init__(self, settings: Settings, client: LLMClient, exclude_declarations: set[int], size: int = 2500):
        self.settings, self.client, self.exclude, self.size = settings, client, exclude_declarations, size
        self.texts: list[str] | None = None
        self.vectors = None

    async def ensure(self):
        """Load and embed the comments once (lazily, on the first search)."""
        if self.texts is not None:
            return
        rows = fetchall(
            self.settings,
            """
            select s.declaration_id, left(regexp_replace(s.comment, '\\s+', ' ', 'g'), 700) c
            from data_snapshot s where s.status in ('OBSERVATION','OBJECTION','REJECTED')
              and length(s.comment) > 60 and s.comment ilike %s
            order by md5(s.id::text) limit %s""",
            ("%étiquet%", self.size + len(self.exclude) + 50),
        )
        self.texts = [r["c"] for r in rows if r["declaration_id"] not in self.exclude][: self.size]
        vecs = await self.client.embed(self.texts, stage="embed_doctrine")
        m = np.array(vecs, dtype=np.float32)
        self.vectors = m / np.linalg.norm(m, axis=1, keepdims=True)

    async def search(self, question: str, k: int = 4) -> list[str]:
        await self.ensure()
        (v,) = await self.client.embed([question], stage="embed_query")
        q = np.array(v, dtype=np.float32)
        q /= np.linalg.norm(q)
        return [self.texts[i] for i in np.argsort(-(self.vectors @ q))[:k]]


class VerificationAgent:
    def __init__(self, settings: Settings, ref: RefData, client: LLMClient, resolver: Resolver, doctrine: Doctrine):
        self.settings, self.ref, self.client, self.resolver, self.doctrine = settings, ref, client, resolver, doctrine

    @staticmethod
    def candidates(findings: list[Finding]) -> list[Finding]:
        """Findings worth verifying: those that could lead to a block. At most 10 per declaration."""
        cands = [f for f in findings if f.severity == Severity.BLOCKING and f.confidence >= 0.5]
        cands += [f for f in findings if f.severity == Severity.MAJOR and f.confidence >= 0.6]
        return cands[:10]

    async def _tool(
        self, name: str, args: dict, decl: DeclarationDTO, docs: list[LabelDocument], label: MergedLabel
    ) -> tuple[str, list[str]]:
        """Execute one tool call. Returns (text result, images to show the agent as data URLs)."""
        ref = self.ref
        if name == "voir_page":
            fi, pg = int(args.get("fichier", 0)), int(args.get("page", 0))
            if fi >= len(docs) or pg >= len(docs[fi].pages):
                return "Fichier ou page inexistant.", []
            zone = ZONES.get(args.get("zone") or "tout")
            rot = int(args.get("rotation") or 0) % 360
            # Tool results cannot carry images: the image is sent in the next user message.
            return (
                f"Image du fichier {fi}, page {pg}, zone {args.get('zone') or 'tout'}, rotation {rot}° : "
                "voir le message suivant."
            ), [docs[fi].page_data_url(pg, crop=zone, max_side=1600, rotation=rot)]
        if name == "transcription":
            fi, pg = int(args.get("fichier", 0)), int(args.get("page", 0))
            if fi >= len(label.files) or pg >= len(label.files[fi].ocr_pages):
                return "Fichier ou page inexistant.", []
            extra = (
                ("\n\n=== Texte lu sur les pages tournées ===\n" + label.extra_text[:6000]) if label.extra_text else ""
            )
            return label.files[fi].ocr_pages[pg][:12000] + extra, []
        if name == "rechercher_referentiel":
            hits = self.resolver.index.fuzzy(args.get("texte", ""), k=8)
            sem = await self.resolver.index.semantic(self.client, args.get("texte", ""), k=8)
            uids = list(dict.fromkeys([u for u, _ in hits] + [u for u, _ in sem]))[:10]
            return json.dumps([self.resolver._describe(u) for u in uids], ensure_ascii=False), []
        if name == "fiche_element":
            el = ref.get(args.get("uid"))
            if el is None:
                return "uid inconnu.", []
            pops = {ref.populations.get(p, {}).get("name", p): v for p, v in el.max_by_population.items()}
            return json.dumps(
                {
                    "uid": el.uid,
                    "type": KIND_FR[el.kind],
                    "nom": el.name,
                    "synonymes": el.synonyms[:8],
                    "statut": STATUS_FR.get(el.status),
                    "a_surveiller": el.is_risky,
                    "actif": el.active,
                    "unite": ref.unit_name(el.unit_id),
                    "doses_max_par_population": pops,
                    "avertissements_obligatoires": el.warnings,
                    "substances": [ref.get(s).name for s in el.substances if ref.get(s)][:15],
                },
                ensure_ascii=False,
            ), []
        if name == "calculer_article":
            comp = composition_from_declaration(decl, ref)
            for uid in args.get("ajouter_uids") or []:
                el = ref.get(uid)
                if el:
                    comp.items.append(CompItem(kind=el.kind, uid=uid, source="label"))
            for q in args.get("quantites") or []:
                ex = next((s for s in comp.computed_substances if s.uid == q.get("uid")), None)
                if ex:
                    ex.quantity = q.get("quantite")
                elif ref.get(q.get("uid")):
                    comp.computed_substances.append(CompSubstance(uid=q["uid"], quantity=q.get("quantite")))
            res = compute_article(comp, ref)
            return json.dumps(
                {"article": res.article, "raisons": res.reasons, "article_declare": decl.article}, ensure_ascii=False
            ), []
        if name == "calculer":
            try:
                return str(safe_calc(str(args.get("expression", "")))), []
            except Exception as e:  # noqa: BLE001
                return f"Erreur : {e}", []
        if name == "convertir":
            v = convert(args.get("valeur"), args.get("de"), args.get("vers"), args.get("substance"))
            return ("conversion impossible" if v is None else f"{v:g} {args.get('vers')}"), []
        if name == "doctrine_instructeurs":
            hits = await self.doctrine.search(args.get("question", ""))
            return "\n---\n".join(hits), []
        return f"Outil inconnu : {name}", []

    # Findings that assert an ABSENCE (nothing to quote): confirming them requires having looked at the label.
    ABSENCE_CODES = ("R-MEN-", "R-WARN-", "R-DOC-NO-FRENCH", "R-DOC-NOT-LABEL", "R-DOC-ILLEGIBLE", "R-ID-")

    def _confirmation_supported(
        self, f: Finding, quote: str | None, label: MergedLabel, looked: bool
    ) -> tuple[bool, str]:
        """Is the agent's "confirmed" verdict backed by proof? Returns (supported, reason if not).

        - absence finding: the agent must have looked at the label image (`voir_page`);
        - presence finding: its quote must exist in the label text AND name the element at stake.
        """
        if f.code.startswith(self.ABSENCE_CODES):
            return (True, "") if looked else (False, "absence confirmed without looking at the label")
        if not quote or quote_in_text(quote, label.text) < 80:
            return False, "quote not found in the label"
        names = []
        for uid in f.refs:
            el = self.ref.get(uid)
            if el:
                names += [el.name.split("(")[0]] + el.synonyms[:6]
        if names and max(fuzz.partial_ratio(normalise(n), normalise(quote)) for n in names if normalise(n)) < 80:
            return False, "the quote does not mention the element at stake"
        return True, ""

    async def verify(
        self, decl: DeclarationDTO, docs: list[LabelDocument], label: MergedLabel, findings: list[Finding]
    ) -> dict:
        """Run the agent loop on the candidate findings and apply its verdicts to them (in place).

        Returns a trace for the run results: turns, verdicts, tool calls.
        """
        cands = self.candidates(findings)
        if not cands:
            return {"ran": False}
        # What the label reading produced, so the agent knows where to look (model input, French keys).
        label_summary = {
            f"fichier_{fi}": {
                "nature": f.extraction.document_kind.value,
                "lisibilite": f.extraction.legibility.value,
                "pages": len(f.ocr_pages),
                "produit": f.extraction.product.model_dump(),
                "posologie": f.extraction.daily_dose.text,
                "ingredients": [i.raw for i in f.extraction.ingredients],
                "composition": [c.raw for c in f.extraction.composition][:40],
                "avertissements": [w.quote for w in f.extraction.warnings][:30],
            }
            for fi, f in enumerate(label.files)
        }
        task = {
            "declaration": decl.summary_for_llm(),
            "article_declare": decl.article,
            "etiquette_lue": label_summary,
            "constats_a_verifier": [
                {
                    "id": f.id,
                    "code": f.code,
                    "gravite": f.severity.value,
                    "titre": f.title,
                    "detail": f.detail,
                    "preuves": [e.model_dump() for e in f.evidence],
                }
                for f in cands
            ],
        }
        messages: list[dict] = [
            {"role": "system", "content": prompt_text("agent_verify.md")},
            {"role": "user", "content": json.dumps(task, ensure_ascii=False)},
        ]
        transcript: list[dict] = []
        output: AgentOutput | None = None
        for turn in range(self.settings.agent_max_turns):
            # On the last turn, only `rendre_verdict` is offered and a tool call is forced.
            last = turn == self.settings.agent_max_turns - 1
            tools = [TOOLS[-1]] if last else TOOLS
            msg = await self.client.chat_tools(
                "agent",
                self.settings.model_agent,
                messages,
                tools,
                tool_choice="any" if last else "auto",
                max_tokens=4000,
            )
            calls = msg.get("tool_calls") or []
            messages.append(
                {"role": "assistant", "content": msg.get("content") or "", "tool_calls": calls}
                if calls
                else {"role": "assistant", "content": msg.get("content") or ""}
            )
            if not calls:
                messages.append({"role": "user", "content": "Appelle l'outil rendre_verdict pour conclure."})
                continue
            images: list[str] = []
            for c in calls:
                name = c["function"]["name"]
                try:
                    args = json.loads(c["function"].get("arguments") or "{}")
                except json.JSONDecodeError:
                    args = {}
                if name == "rendre_verdict":
                    try:
                        output = AgentOutput.model_validate(
                            {"verdicts": args.get("verdicts", []), "new_findings": args.get("new_findings", [])}
                        )
                    except Exception:  # noqa: BLE001
                        output = None
                    messages.append({"role": "tool", "tool_call_id": c["id"], "name": name, "content": "ok"})
                    transcript.append({"tool": name, "args": args})
                    continue
                result, imgs = await self._tool(name, args, decl, docs, label)
                images += imgs
                transcript.append({"tool": name, "args": args, "result": result[:500]})
                messages.append({"role": "tool", "tool_call_id": c["id"], "name": name, "content": result})
            if output is not None:
                break
            if images:
                messages.append(
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": "Image(s) demandée(s) :"}]
                        + [{"type": "image_url", "image_url": u} for u in images[:3]],
                    }
                )
        by_id = {f.id: f for f in findings}
        applied = []
        looked = any(t["tool"] == "voir_page" for t in transcript)
        for v in output.verdicts if output else []:
            f = by_id.get(v.finding_id)
            if f is None:
                continue
            # The agent's confirmation must itself be proven (real case: "Magnesium 56 mg" wrongly
            # confirmed as "Manganese 56 mg"):
            #  - PRESENCE finding: its quote must exist in the label and name the element at stake;
            #  - ABSENCE finding: the agent must have looked at the label image.
            if v.verdict == "confirmed":
                ok, why = self._confirmation_supported(f, v.quote, label, looked)
                if not ok:
                    v = v.model_copy(
                        update={
                            "verdict": "uncertain",
                            "explanation": f"[confirmation not supported: {why}] " + v.explanation,
                        }
                    )
            f.verified = v.verdict
            f.verification_note = v.explanation[:600]
            # A confirmation raises the confidence (capped at 0.99); an uncertain verdict lowers it.
            if v.verdict == "confirmed":
                f.confidence = round(max(f.confidence, min(v.confidence, 0.99)), 3)
            elif v.verdict == "uncertain":
                f.confidence = round(f.confidence * 0.7, 3)
            applied.append(v.model_dump())
        return {
            "ran": True,
            "turns": len([m for m in messages if m["role"] == "assistant"]),
            "verdicts": applied,
            "new_findings": output.new_findings if output else [],
            "completed": output is not None,
            "transcript": transcript,
        }
