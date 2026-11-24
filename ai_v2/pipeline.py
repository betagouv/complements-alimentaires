"""Orchestrator: one declaration -> a reasoned BLOCK / PASS decision, with a full trace.

  0 SQL triage -> 1 download + OCR (cached) -> 2 blind structured extraction (cached)
  -> 3 entity resolution -> 4 deterministic rules -> 5 verification by the agent
  -> 6 decision + message to the declarant

Everything is async: several declarations, and several files per declaration, run in parallel.
A technical failure (network, API, database) gives an ERROR to be replayed, never a block.
"""

from __future__ import annotations

import asyncio
import time
import traceback

from .agent import Doctrine, VerificationAgent
from .cache import Cache
from .config import Settings
from .db import run_db
from .decision import decide
from .declarations import DeclarationDTO
from .documents import DocumentError, DocumentStore
from .extract import MergedLabel, extract_document, ocr_rotated
from .label_index import LabelIndex
from .llm import CURRENT_KEY, BudgetExceeded, LLMClient, Usage
from .refdata import load_refdata
from .resolve import ResolveQuery, Resolver
from .rules import (
    CORE_MENTIONS,
    Context,
    LabelRow,
    match_rows_to_declaration,
    rule_alcohol_warning,
    rule_claims,
    rule_completeness,
    rule_counterfactual_article,
    rule_daily_dose,
    rule_document,
    rule_doses,
    rule_drops_in_ml,
    rule_identity,
    rule_mentions,
    rule_specific_warnings,
)
from .schemas import FraudType, MentionStatus, Severity
from .triage import triage


class Pipeline:
    """Holds the long-lived objects of a run (client, cache, reference data, indexes) and analyses
    declarations with them. Call aclose() at the end: it also saves the learned aliases and the
    label index."""

    def __init__(self, settings: Settings, exclude_from_doctrine: set[int] | None = None):
        self.settings = settings
        self.cache = Cache(settings.data_dir / "cache" / "cache.sqlite")
        self.usage = Usage(budget_usd=settings.budget_usd)
        self.client = LLMClient(settings, self.cache, self.usage)
        self.docs = DocumentStore(settings)
        self.ref = load_refdata(settings)
        self.resolver = Resolver(settings, self.ref, self.client, self.cache)
        # Declarations under evaluation are excluded from the instructor-comment RAG (no leakage).
        self.doctrine = Doctrine(settings, self.client, exclude_from_doctrine or set())
        self.agent = VerificationAgent(settings, self.ref, self.client, self.resolver, self.doctrine)
        self.label_index = LabelIndex(settings.data_dir / "label_index.json")

    async def aclose(self) -> None:
        self.resolver.aliases.save()
        self.label_index.save()
        await self.client.aclose()
        await self.docs.aclose()

    # ------------------------------------------------------------------------------------
    async def analyze(self, decl: DeclarationDTO) -> dict:
        """Analyse one declaration. Never raises (except BudgetExceeded): errors become an ERROR decision."""
        CURRENT_KEY.set(decl.key)
        t0 = time.monotonic()
        out: dict = {
            "key": decl.key,
            "declaration_id": decl.declaration_id,
            "snapshot_id": decl.snapshot_id,
            "source": decl.source,
            "name": decl.name,
            "brand": decl.brand,
            "declared_article": decl.article,
            "file_errors": [],
        }
        try:
            await self._analyze(decl, out)
        except BudgetExceeded:
            raise
        except Exception as e:  # noqa: BLE001 - one failing declaration must not stop the run
            out["decision"] = {
                "decision": "ERROR",
                "risk_score": None,
                "blocking_findings": [],
                "reason_codes": [],
                "message_to_declarant": "",
            }
            out["error"] = f"{type(e).__name__}: {e}"
            out["traceback"] = traceback.format_exc()[-4000:]
        out["cost_usd"] = round(self.usage.cost_for(decl.key), 5)
        out["latency_s"] = round(time.monotonic() - t0, 1)
        return out

    async def _analyze(self, decl: DeclarationDTO, out: dict) -> None:
        s, ref = self.settings, self.ref
        tri = await run_db(triage, s, ref, decl)
        out["triage"] = tri
        labels = decl.labels[: s.max_label_files]

        # ---------------- stages 1-2: download, OCR and extraction of each label file, in parallel
        async def load_one(att):
            try:
                doc = await self.docs.load(att.url)
                fe = await extract_document(self.client, s, doc)
                return doc, fe
            except BudgetExceeded:
                raise
            except DocumentError as e:  # the FILE is the problem (unknown format, corrupt, too large)
                out["file_errors"].append({"url": att.url, "error": f"DocumentError: {e}", "kind": "document"})
                return None
            except Exception as e:  # noqa: BLE001 - technical failure (network, API): never a reason to block
                out["file_errors"].append({"url": att.url, "error": f"{type(e).__name__}: {e}", "kind": "technical"})
                return None

        loaded = [x for x in await asyncio.gather(*(load_one(a) for a in labels)) if x]
        if labels and not loaded and any(e.get("kind") == "technical" for e in out["file_errors"]):
            raise RuntimeError("label files not processed for a technical reason: replay, no decision")
        docs = [d for d, _ in loaded]
        label = MergedLabel(files=[fe for _, fe in loaded])
        # Before concluding that a mandatory statement is absent, re-read the rotated pages
        # (text blocks printed at 90/180/270 degrees, common on multilingual labels).
        if loaded and any(label.mention(k)[0].status == MentionStatus.absent for k in CORE_MENTIONS):
            label.extra_text = "\n".join(await asyncio.gather(*(ocr_rotated(self.client, d) for d in docs)))
        reused = await asyncio.to_thread(
            self.label_index.check_and_add, decl, docs, "\n".join(f.full_text for f in label.files)
        )
        out["files"] = [
            {
                "url": fe.url,
                "sha256": fe.sha256,
                "kind": fe.kind,
                "n_pages_total": fe.n_pages_total,
                "dhash": [p.dhash for p in d.pages],
                "grounding": {k: v for k, v in fe.grounding.items() if not k.endswith("_flags")},
                "extraction": fe.extraction.model_dump(mode="json"),
            }
            for d, fe in loaded
        ]

        # ---------------- stage 3: resolution (ingredient list rows first, then composition rows)
        ing = label.ingredients()
        comp = label.composition()
        queries = [
            ResolveQuery(
                raw=i.raw,
                name=i.name,
                botanical=i.botanical_name,
                part=i.plant_part,
                preparation=i.preparation,
                e_number=i.e_number,
                functional_class=i.functional_class,
                context="ingredient_list",
                is_active=i.is_active,
            )
            for _, i, _ in ing
        ]
        queries += [ResolveQuery(raw=r.raw, name=r.name, context="composition") for _, r, _ in comp]
        resolutions = await self.resolver.resolve_many(queries) if queries else []
        rows = [
            LabelRow(
                file_index=fi,
                kind="ingredient",
                raw=i.raw,
                name=i.name,
                page=i.page,
                grounded=g,
                resolution=res,
                ingredient=i,
            )
            for (fi, i, g), res in zip(ing, resolutions[: len(ing)])
        ]
        rows += [
            LabelRow(
                file_index=fi,
                kind="composition",
                raw=r.raw,
                name=r.name,
                page=r.page,
                grounded=g,
                resolution=res,
                row=r,
            )
            for (fi, r, g), res in zip(comp, resolutions[len(ing) :])
        ]

        # ---------------- stage 4: rules
        ctx = Context(settings=s, ref=ref, decl=decl, label=label, rows=rows)
        if not labels:
            ctx.add(
                "R-DOC-NO-LABEL",
                Severity.BLOCKING,
                "fake_label",
                0.95,
                "Aucune étiquette fournie",
                "La déclaration ne comporte pas de fichier d'étiquetage.",
                grounded_=True,
            )
        elif not loaded:
            # Only reached when every failure is a DocumentError (technical failures raised above).
            ctx.add(
                "R-DOC-UNREADABLE",
                Severity.BLOCKING,
                "fake_label",
                0.85,
                "Étiquette inexploitable",
                "Aucun des fichiers d'étiquetage n'a pu être lu (format non reconnu, fichier corrompu ou trop lourd).",
                grounded_=True,
            )
        else:
            match_rows_to_declaration(ctx)
            # Order matters: rule_counterfactual_article reuses the quantities computed by rule_doses.
            for rule in (
                rule_completeness,
                rule_doses,
                rule_counterfactual_article,
                rule_mentions,
                rule_document,
                rule_identity,
                rule_daily_dose,
                rule_drops_in_ml,
                rule_alcohol_warning,
                rule_claims,
            ):
                rule(ctx)
            await rule_specific_warnings(ctx, self.client)
            for other in reused:
                ctx.add(
                    "R-DOC-REUSED",
                    Severity.BLOCKING,
                    FraudType.fake_label,
                    0.9,
                    "Étiquette identique à celle d'un autre produit déclaré",
                    f"Le visuel ET le texte de l'étiquette sont identiques à ceux de la déclaration "
                    f"n° {other['declaration_id']} « {other['name']} », un produit différent.",
                    grounded_=True,
                )

        # ---------------- stage 5: verification by the agent
        agent_info = {"ran": False}
        if s.agent_enabled and loaded:
            try:
                agent_info = await self.agent.verify(decl, docs, label, ctx.findings)
            except BudgetExceeded:
                raise
            except Exception as e:  # noqa: BLE001 - without the agent, findings stay unverified
                agent_info = {"ran": False, "error": f"{type(e).__name__}: {e}"}
        out["agent"] = agent_info

        # ---------------- stage 6: decision + full trace
        decision = decide(ctx.findings, s, decl.name, ctx.facts, prior=tri["prior"])
        out["decision"] = decision.model_dump()
        out["findings"] = [f.model_dump(mode="json") for f in ctx.findings]
        out["facts"] = {k: v for k, v in ctx.facts.items() if not k.startswith("_")}
        out["rows"] = [
            {
                "kind": r.kind,
                "raw": r.raw,
                "name": r.name,
                "page": r.page,
                "file": r.file_index,
                "grounded": r.grounded,
                "uid": r.resolution.uid,
                "element": ref.get(r.resolution.uid).label() if ref.get(r.resolution.uid) else None,
                "confidence": r.resolution.confidence,
                "method": r.resolution.method,
                "part_id": r.resolution.part_id,
                "matched_declared": r.matched_declared,
                "match_via": r.match_via,
            }
            for r in rows
        ]
        out["declared_items"] = [it.model_dump() for it in decl.items]

        # ---------------- alias learning: only when the model AND the declarant agree
        for r in rows:
            if r.match_via == "uid" and r.resolution.method == "llm" and r.resolution.confidence >= 0.9:
                self.resolver.aliases.learn(r.raw, r.resolution.uid, "llm+declared")

    async def run_many(self, decls: list[DeclarationDTO], on_result=None) -> list[dict]:
        """Analyse many declarations concurrently (max_concurrent_declarations at a time).

        `on_result` is called as soon as each result is ready (used to save results incrementally).
        When the budget is reached, the declarations not started yet are skipped.
        """
        sem = asyncio.Semaphore(self.settings.max_concurrent_declarations)
        results: list[dict] = []
        stop = asyncio.Event()

        async def one(d):
            if stop.is_set():
                return
            async with sem:
                if stop.is_set():
                    return
                try:
                    r = await self.analyze(d)
                except BudgetExceeded as e:
                    stop.set()
                    r = {
                        "key": d.key,
                        "declaration_id": d.declaration_id,
                        "budget_stop": str(e),
                        "decision": {"decision": "ERROR"},
                    }
                results.append(r)
                if on_result:
                    on_result(r)

        await asyncio.gather(*(one(d) for d in decls))
        return results
