"""Stage 3: entity resolution (label wording -> reference data identifier).

Cascade, cheapest first:
  1. learned alias table             (normalised wording -> uid)
  2. E-number / botanical binomial   (exact indexes)
  3. exact name or synonym           (normalised)
  4. candidates: fuzzy (trigram-like, local equivalent of pg_trgm) + semantic (embeddings, local
     equivalent of pgvector), merged by reciprocal rank fusion (RRF)
  5. a small model PICKS one uid among the item's candidates (or NONE); a uid outside the
     candidates is rejected. The whole reference data is never sent in a prompt.

The candidate descriptions sent to the model use French keys and labels (model input).
"""

from __future__ import annotations

import asyncio
import json
import re
import threading
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from rapidfuzz import fuzz, process

from .cache import Cache
from .config import Settings, prompt_hash, prompt_text
from .llm import LLMClient
from .refdata import KIND_FR, RefData
from .schemas import Resolution, ResolveBatch
from .text import e_numbers, normalise

# French labels of the element statuses (shown to the models).
STATUS_FR = {1: "autorisé", 2: "NON autorisé", 3: "sans objet", 99: "retiré", None: "?"}
# Words describing the part or the preparation of a plant (French): stripped to retry an exact match
# on the bare name ("extrait sec de racine de curcuma" -> "curcuma").
PREP_WORDS = re.compile(
    r"\b(extrait|extraits|sec|seche|secs|poudre|de|du|des|d|la|le|les|huile|essentielle|teinture|mere|titre|titree|"
    r"standardise|standardisee|bio|biologique|micronise|naturel|naturelle|concentre|jus|racine|racines|feuille|feuilles|"
    r"fleur|fleurs|fruit|fruits|graine|graines|ecorce|rhizome|partie|parties|aerienne|aeriennes|sommite|sommites|"
    r"fleurie|fleuries|plante|entiere|baie|baies|pepin|pepins|tige|tiges|bulbe|gousse|zeste|peau)\b"
)


@dataclass
class ResolveQuery:
    raw: str
    name: str
    botanical: str | None = None
    part: str | None = None
    preparation: str | None = None
    e_number: str | None = None
    functional_class: str | None = None
    context: str = "ingredient_list"  # ingredient_list | composition
    is_active: bool = True


class AliasStore:
    """Learned aliases: normalised wording -> uid, with provenance. Grows run after run.

    An alias is only learned when the model's choice AND the declarant's declaration agree
    (pipeline.Pipeline._analyze), so a single wrong answer cannot poison the table.
    """

    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.Lock()
        self.data: dict[str, dict] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

    def get(self, text: str) -> str | None:
        e = self.data.get(normalise(text))
        return e["uid"] if e and e.get("count", 0) >= 1 else None

    def learn(self, text: str, uid: str, source: str) -> None:
        k = normalise(text)
        if not k:
            return
        with self._lock:
            e = self.data.get(k)
            if e and e["uid"] != uid:
                e["conflicts"] = e.get("conflicts", 0) + 1
                if e["conflicts"] >= e.get("count", 1):
                    del self.data[k]  # two sources disagree: stop using the alias
            elif e:
                e["count"] += 1
            else:
                self.data[k] = {"uid": uid, "source": source, "count": 1}

    def save(self) -> None:
        with self._lock:
            self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=0), encoding="utf-8")


class CandidateIndex:
    """In-memory search indexes over the reference data names and synonyms."""

    def __init__(self, ref: RefData):
        self.ref = ref
        pairs = ref.searchable_strings()
        self.texts = [t for t, _ in pairs]
        self.uids = [u for _, u in pairs]
        self.norm = [normalise(t) for t in self.texts]
        self.exact: dict[str, set[str]] = {}
        self.binomial: dict[str, set[str]] = {}  # "genus species" -> plants / micro-organisms
        self.e_index: dict[str, set[str]] = {}  # "e464" -> additives
        for n, uid in zip(self.norm, self.uids):
            self.exact.setdefault(n, set()).add(uid)
            el = ref.elements[uid]
            if el.kind in ("plant", "microorganism"):
                toks = n.split()
                if len(toks) >= 2:
                    self.binomial.setdefault(" ".join(toks[:2]), set()).add(uid)
            for code in e_numbers(n):
                if el.kind == "ingredient":
                    self.e_index.setdefault(code.lower(), set()).add(uid)
        self.vectors: np.ndarray | None = None  # embeddings, computed lazily (first semantic query)
        self._vec_lock = asyncio.Lock()

    def fuzzy(self, text: str, k: int = 12) -> list[tuple[str, float]]:
        """Top-k uids by fuzzy string similarity (best score per uid)."""
        q = normalise(text)
        if not q:
            return []
        res = process.extract(q, self.norm, scorer=fuzz.WRatio, limit=k * 3)
        best: dict[str, float] = {}
        for _, score, idx in res:
            uid = self.uids[idx]
            best[uid] = max(best.get(uid, 0), score)
        return sorted(best.items(), key=lambda x: -x[1])[:k]

    async def ensure_vectors(self, client: LLMClient) -> None:
        async with self._vec_lock:
            if self.vectors is None:
                vecs = await client.embed(self.texts, stage="embed_refdata")
                m = np.array(vecs, dtype=np.float32)
                self.vectors = m / np.linalg.norm(m, axis=1, keepdims=True)

    async def semantic(self, client: LLMClient, text: str, k: int = 12) -> list[tuple[str, float]]:
        """Top-k uids by cosine similarity of embeddings (best score per uid)."""
        await self.ensure_vectors(client)
        (v,) = await client.embed([text], stage="embed_query")
        q = np.array(v, dtype=np.float32)
        q /= np.linalg.norm(q)
        sims = self.vectors @ q
        best: dict[str, float] = {}
        for idx in np.argsort(-sims)[: k * 3]:
            uid = self.uids[idx]
            best[uid] = max(best.get(uid, 0), float(sims[idx]))
        return sorted(best.items(), key=lambda x: -x[1])[:k]


def _rrf(*rankings: list[tuple[str, float]], k: int = 60, top: int = 12) -> list[str]:
    """Reciprocal rank fusion: merges rankings whose scores are not comparable (fuzzy vs cosine)."""
    score: dict[str, float] = {}
    for ranking in rankings:
        for rank, (uid, _) in enumerate(ranking):
            score[uid] = score.get(uid, 0) + 1 / (k + rank)
    return [u for u, _ in sorted(score.items(), key=lambda x: -x[1])[:top]]


class Resolver:
    def __init__(self, settings: Settings, ref: RefData, client: LLMClient, cache: Cache):
        self.settings = settings
        self.ref = ref
        self.client = client
        self.cache = cache
        self.index = CandidateIndex(ref)
        self.aliases = AliasStore(settings.data_dir / "aliases.json")

    # ------------------------------------------------------------------ plant parts
    def resolve_part(self, plant_uid: str | None, part_text: str | None) -> int | None:
        """Plant part id from its wording, preferring the parts allowed for that plant."""
        if not part_text:
            return None
        q = normalise(part_text)
        names = {pid: normalise(n) for pid, n in self.ref.plant_parts.items()}
        allowed = self.ref.parts_by_plant.get(plant_uid.split(":")[1], {}) if plant_uid else {}
        pool = {pid: n for pid, n in names.items() if pid in allowed} or names
        best = process.extractOne(q, pool, scorer=fuzz.WRatio)
        if best and best[1] >= 85:
            return int(best[2])
        return None

    # ------------------------------------------------------------------ deterministic
    def _deterministic(self, q: ResolveQuery) -> Resolution | None:
        """Steps 1-3 of the cascade. Only returns a match when it is unambiguous."""
        for text in (q.raw, q.name):
            uid = self.aliases.get(text)
            if uid and uid in self.ref.elements:
                return Resolution(text=q.raw, uid=uid, confidence=0.97, method="alias")
        codes = [c.lower() for c in e_numbers(q.e_number or "") + e_numbers(q.raw)]
        for c in codes:
            hits = self.index.e_index.get(c)
            if hits and len(hits) == 1:
                return Resolution(text=q.raw, uid=next(iter(hits)), confidence=0.97, method="e_number")
        if q.botanical:
            toks = normalise(q.botanical).split()
            if len(toks) >= 2:
                hits = self.index.binomial.get(" ".join(toks[:2]))
                if hits and len(hits) == 1:
                    return Resolution(text=q.raw, uid=next(iter(hits)), confidence=0.96, method="botanical")
        for text in (q.name, q.raw, PREP_WORDS.sub(" ", normalise(q.name))):
            hits = self.index.exact.get(normalise(text))
            if hits:
                hits = {h for h in hits if not self.ref.elements[h].is_obsolete} or hits
                if len(hits) == 1:
                    return Resolution(text=q.raw, uid=next(iter(hits)), confidence=0.95, method="exact")
                pref = self._prefer_by_context(hits, q)
                if pref:
                    return Resolution(
                        text=q.raw, uid=pref, confidence=0.9, method="exact_context", candidates=sorted(hits)
                    )
        return None

    def _prefer_by_context(self, uids: set[str], q: ResolveQuery) -> str | None:
        """Several elements carry exactly this name (e.g. the substance "zinc" and an ingredient):
        in a composition table we want the substance, in an ingredient list the ingredient/plant."""
        kinds = {u: self.ref.elements[u].kind for u in uids}
        wanted = (
            ("substance",) if q.context == "composition" else ("plant", "ingredient", "microorganism", "substance")
        )
        for w in wanted:
            cand = [u for u, k in kinds.items() if k == w]
            if len(cand) == 1:
                return cand[0]
        return None

    # ------------------------------------------------------------------ candidates + LLM
    async def _candidates(self, q: ResolveQuery) -> list[str]:
        """Step 4: up to 12 candidate uids, fuzzy and semantic rankings merged by RRF."""
        texts = [t for t in {q.name, q.raw, q.botanical or ""} if t]
        fuzzy = []
        for t in texts:
            fuzzy += self.index.fuzzy(t)
        fuzzy.sort(key=lambda x: -x[1])
        sem = await self.index.semantic(self.client, f"{q.raw} | {q.botanical or ''} | {q.functional_class or ''}")
        return _rrf(fuzzy, sem, top=12)

    def _describe(self, uid: str) -> dict:
        """Short description of a candidate, as shown to the models (French keys: model input)."""
        el = self.ref.elements[uid]
        return {
            "uid": uid,
            "type": KIND_FR[el.kind],
            "nom": el.name,
            "synonymes": el.synonyms[:5],
            "statut": STATUS_FR.get(el.status, "?"),
        }

    async def resolve_many(self, queries: list[ResolveQuery]) -> list[Resolution]:
        """Resolve all the rows of a label at once (one model call per batch of 15 unresolved items)."""
        results: list[Resolution | None] = [None] * len(queries)
        pending: list[tuple[int, ResolveQuery, list[str], str]] = []
        for i, q in enumerate(queries):
            r = self._deterministic(q)
            if r:
                results[i] = r
        cand_lists = await asyncio.gather(*(self._candidates(q) for i, q in enumerate(queries) if results[i] is None))
        it = iter(cand_lists)
        for i, q in enumerate(queries):
            if results[i] is not None:
                continue
            cands = next(it)
            # Cached per item (query + candidates), so that batching does not affect cache hits.
            key = self.cache.key(
                "resolve",
                model=self.settings.model_resolve,
                prompt=prompt_hash("resolve.md"),
                q=q.__dict__,
                cands=cands,
            )
            hit = self.cache.get(key)
            if hit is not None:
                results[i] = Resolution.model_validate(hit)
            else:
                pending.append((i, q, cands, key))

        for chunk_start in range(0, len(pending), 15):
            chunk = pending[chunk_start : chunk_start + 15]
            payload = [
                {
                    "index": n,
                    "libelle": q.raw,
                    "nom": q.name,
                    "binome": q.botanical,
                    "partie": q.part,
                    "preparation": q.preparation,
                    "code_E": q.e_number,
                    "categorie": q.functional_class,
                    "contexte": q.context,
                    "candidats": [self._describe(u) for u in cands],
                }
                for n, (_, q, cands, _) in enumerate(chunk)
            ]
            out: ResolveBatch = await self.client.chat_json(
                "resolve",
                self.settings.model_resolve,
                [
                    {"role": "system", "content": prompt_text("resolve.md")},
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
                ],
                ResolveBatch,
                max_tokens=4000,
            )
            by_index = {c.index: c for c in out.choices}
            for n, (i, q, cands, key) in enumerate(chunk):
                c = by_index.get(n)
                # Step 5 guard: a uid that was not among this item's candidates is discarded.
                uid = c.uid if c and c.uid in cands else None
                res = Resolution(
                    text=q.raw,
                    uid=uid,
                    # For NONE, the confidence is the model's certainty that no candidate matches.
                    confidence=(c.confidence if c else 0.0)
                    if uid
                    else (c.confidence if c and c.uid == "NONE" else 0.0),
                    method="llm" if uid else "none",
                    candidates=cands,
                    reason=c.reason if c else "",
                )
                self.cache.set(key, res.model_dump())
                results[i] = res

        for q, r in zip(queries, results):
            if r and r.uid and self.ref.elements[r.uid].kind == "plant":
                r.part_id = self.resolve_part(r.uid, q.part)
        return results  # type: ignore[return-value]
