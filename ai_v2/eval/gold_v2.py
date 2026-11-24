"""Import of the hand-annotated dataset (about 100 labels), as soon as it is available.

Accepted format: CSV (separator , or ;) or JSONL, one line per declaration, columns:
  declaration_id   (required)
  expected_block   (required: oui/non, true/false, 1/0, BLOCK/PASS)
  snapshot_id      (optional: replays the state at that snapshot; otherwise the current state)
  fraud_types      (optional: list separated by | among fake_label, undeclared_ingredients,
                    article_bypass, dose_underdeclared, label_noncompliance)
  notes            (optional)

  python -m ai_v2.cli gold-import annotations.csv    -> <data_dir>/gold/gold_v2.jsonl
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .gold_v1 import GoldComment, GoldEntry, GoldIssue, IssueCategory

# Annotated fraud type -> issue category, so that per-category recall works like on gold v1.
FRAUD_TO_CATEGORY = {
    "fake_label": IssueCategory.label_other_product,
    "undeclared_ingredients": IssueCategory.undeclared_ingredient,
    "article_bypass": IssueCategory.undeclared_ingredient,
    "dose_underdeclared": IssueCategory.dose_inconsistency,
    "label_noncompliance": IssueCategory.missing_mention,
}


def _bool(v) -> bool:
    """Lenient yes/no parsing (French and English spellings)."""
    return str(v).strip().lower() in ("1", "true", "oui", "yes", "block", "bloquer", "frauduleuse", "fraude")


def import_gold_v2(path: Path) -> list[GoldEntry]:
    if path.suffix.lower() in (".jsonl", ".json"):
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]  # noqa: E741
    else:
        text = path.read_text(encoding="utf-8-sig")
        dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",;\t")
        rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    out = []
    for r in rows:
        did = int(r["declaration_id"])
        snap = int(r["snapshot_id"]) if r.get("snapshot_id") else None
        frauds = [f.strip() for f in str(r.get("fraud_types") or "").split("|") if f.strip()]
        issues = [
            GoldIssue(category=FRAUD_TO_CATEGORY.get(f, IssueCategory.other_label), elements=[], detail=f)
            for f in frauds
        ]
        exp = _bool(r["expected_block"])
        out.append(
            GoldEntry(
                key=f"snap:{snap}" if snap else f"decl:{did}",
                split="gold_v2",
                snapshot_id=snap or 0,
                declaration_id=did,
                expected_block=exp,
                comment=str(r.get("notes") or ""),
                structured=GoldComment(label_related=exp, issues=issues, should_block=exp) if issues else None,
            )
        )
    return out
