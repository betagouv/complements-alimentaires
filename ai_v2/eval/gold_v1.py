"""Gold set v1, built from instructor decisions (no manual annotation).

- POSITIVES: snapshots where an instructor blocked the declaration for a label-related reason
  ("Incohérences entre le dossier et l'étiquetage", "Absence ou non conformité de l'étiquetage").
  We replay the composition AND the label AS THEY WERE when the instructor blocked it
  (snapshot.json_declaration), because the declarant has often fixed them since.
- NEGATIVES: declarations authorised by an instructor (AUTHORIZE_NO_VISA / visa) with NO block
  anywhere in their history: a human read the file and found it compliant.
- PROD: recent automatically validated article 15 declarations (unknown truth), to measure the
  block rate the pipeline would have in production.

The instructor's comment is structured by an LLM into expected findings (category, elements), so
that recall can be measured per fraud type.
"""

from __future__ import annotations

import asyncio
import json
import random
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field

from ..config import Settings, prompt_hash, prompt_text
from ..db import fetchall
from ..llm import LLMClient

# Blocking reasons as stored in the database.
LABEL_REASONS = ["Incohérences entre le dossier et l'étiquetage", "Absence ou non conformité de l'étiquetage"]


# Categories of issues found in instructor comments (see prompts/gold_structure.md).
# No class docstrings on IssueCategory, GoldIssue and GoldComment: they are part of the JSON schema
# sent to the model, like their French field descriptions.
class IssueCategory(str, Enum):
    undeclared_ingredient = "undeclared_ingredient"
    missing_mention = "missing_mention"
    missing_specific_warning = "missing_specific_warning"
    quantities_missing_on_label = "quantities_missing_on_label"
    dose_inconsistency = "dose_inconsistency"
    dose_over_max = "dose_over_max"
    label_other_product = "label_other_product"
    djr_or_galenic_inconsistency = "djr_or_galenic_inconsistency"
    claims = "claims"
    other_label = "other_label"
    not_label = "not_label"


class GoldIssue(BaseModel):
    category: IssueCategory
    elements: list[str] = Field(description="Ingrédients/mentions/substances concernés, tels que nommés")
    detail: str


class GoldComment(BaseModel):
    label_related: bool = Field(
        description="Le commentaire signale au moins un problème visible en lisant l'étiquette ou en la comparant au dossier"
    )
    issues: list[GoldIssue]
    should_block: bool = Field(
        description="Un contrôle automatique aurait-il eu raison de refuser la validation automatique ?"
    )


class GoldEntry(BaseModel):
    """One evaluation case."""

    key: str  # "snap:<snapshot id>" (replayed at that snapshot) or "decl:<id>" (current state)
    split: str  # positive | negative | prod (gold v1), gold_v2, adhoc
    snapshot_id: int
    declaration_id: int
    article: str | None = None
    expected_block: bool | None = None  # None = unknown truth (prod split)
    blocking_reasons: list[str] = Field(default_factory=list)
    comment: str = ""  # instructor comment (never shown to the pipeline)
    structured: GoldComment | None = None
    n_labels: int = 0


def _candidates_positive(settings: Settings, limit: int) -> list[dict]:
    # First label-related block of each declaration (historical Teleicare declarations excluded).
    return fetchall(
        settings,
        """
        select distinct on (s.declaration_id) s.id, s.declaration_id, s.blocking_reasons, s.comment,
               s.json_declaration::jsonb->>'article' article,
               (select count(*) from jsonb_array_elements(s.json_declaration::jsonb->'attachments') a where a->>'type'='LABEL') n_labels
        from data_snapshot s join data_declaration d on d.id = s.declaration_id
        where s.status in ('OBSERVATION','OBJECTION','REJECTED') and s.blocking_reasons && %s
          and length(s.comment) > 40 and d.siccrf_id is null
        order by s.declaration_id, s.id
    """,
        (LABEL_REASONS,),
    )


def _candidates_negative(settings: Settings, limit: int) -> list[dict]:
    # Authorised by an instructor, never blocked; random but reproducible order (md5 of the id).
    return fetchall(
        settings,
        """
        select s.id, s.declaration_id, s.json_declaration::jsonb->>'article' article,
               (select count(*) from jsonb_array_elements(s.json_declaration::jsonb->'attachments') a where a->>'type'='LABEL') n_labels
        from data_snapshot s join data_declaration d on d.id = s.declaration_id
        where s.action in ('AUTHORIZE_NO_VISA','APPROVE_VISA') and s.status = 'AUTHORIZED' and d.siccrf_id is null
          and not exists (select 1 from data_snapshot o where o.declaration_id = s.declaration_id
                          and (o.status in ('OBSERVATION','OBJECTION','REJECTED') or cardinality(o.blocking_reasons) > 0))
        order by md5(s.id::text) limit %s
    """,
        (limit * 3,),
    )


def _candidates_prod(settings: Settings, limit: int) -> list[dict]:
    # Automatically validated in the last 60 days.
    return fetchall(
        settings,
        """
        select s.id, s.declaration_id, s.json_declaration::jsonb->>'article' article,
               (select count(*) from jsonb_array_elements(s.json_declaration::jsonb->'attachments') a where a->>'type'='LABEL') n_labels
        from data_snapshot s join data_declaration d on d.id = s.declaration_id
        where s.action = 'AUTOMATICALLY_AUTHORIZE' and d.siccrf_id is null and s.creation_date > now() - interval '60 days'
        order by md5(s.id::text) limit %s
    """,
        (limit * 3,),
    )


async def structure_comment(client: LLMClient, settings: Settings, comment: str, reasons: list[str]) -> GoldComment:
    """Turn an instructor's free-text comment into expected findings (cached)."""
    return await client.chat_json(
        "gold_structure",
        settings.model_gold,
        [
            {"role": "system", "content": prompt_text("gold_structure.md")},
            {
                "role": "user",
                "content": json.dumps({"motifs_de_blocage": reasons, "commentaire": comment}, ensure_ascii=False),
            },
        ],
        GoldComment,
        max_tokens=2000,
        cache_parts={"prompt": prompt_hash("gold_structure.md"), "comment": comment, "reasons": reasons},
    )


async def build_gold_v1(
    client: LLMClient, settings: Settings, n_pos: int = 50, n_neg: int = 30, n_prod: int = 20, seed: int = 42
) -> list[GoldEntry]:
    rng = random.Random(seed)
    pos_rows = [r for r in _candidates_positive(settings, n_pos) if 1 <= r["n_labels"] <= settings.max_label_files]
    rng.shuffle(pos_rows)
    pool = pos_rows[: n_pos * 3]
    structured = await asyncio.gather(
        *(structure_comment(client, settings, r["comment"], r["blocking_reasons"]) for r in pool)
    )
    pos: list[GoldEntry] = []
    by_cat: dict[str, list[GoldEntry]] = {}
    for r, sc in zip(pool, structured):
        # Keep only blocks that a label check could have caught (not a missing lab report, etc.).
        if not (sc.label_related and sc.should_block):
            continue
        e = GoldEntry(
            key=f"snap:{r['id']}",
            split="positive",
            snapshot_id=r["id"],
            declaration_id=r["declaration_id"],
            article=r["article"],
            expected_block=True,
            blocking_reasons=r["blocking_reasons"],
            comment=r["comment"],
            structured=sc,
            n_labels=r["n_labels"],
        )
        main = next((i.category.value for i in sc.issues if i.category != IssueCategory.not_label), "other_label")
        by_cat.setdefault(main, []).append(e)
    # Stratification: pick from each category in turn (rarest first) so that every type is covered
    while len(pos) < n_pos and any(by_cat.values()):
        for cat in sorted(by_cat, key=lambda c: len(by_cat[c])):
            if by_cat[cat] and len(pos) < n_pos:
                pos.append(by_cat[cat].pop(0))

    neg = [
        GoldEntry(
            key=f"snap:{r['id']}",
            split="negative",
            snapshot_id=r["id"],
            declaration_id=r["declaration_id"],
            article=r["article"],
            expected_block=False,
            n_labels=r["n_labels"],
        )
        for r in _candidates_negative(settings, n_neg)
        if 1 <= r["n_labels"] <= settings.max_label_files
    ][:n_neg]
    prod = [
        GoldEntry(
            key=f"snap:{r['id']}",
            split="prod",
            snapshot_id=r["id"],
            declaration_id=r["declaration_id"],
            article=r["article"],
            expected_block=None,
            n_labels=r["n_labels"],
        )
        for r in _candidates_prod(settings, n_prod)
        if 1 <= r["n_labels"] <= settings.max_label_files
    ][:n_prod]
    return pos + neg + prod


def save_gold(entries: list[GoldEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(e.model_dump_json() + "\n")


def load_gold(path: Path) -> list[GoldEntry]:
    return [
        GoldEntry.model_validate_json(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
