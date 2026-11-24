"""Parity of the pure article calculation with the app: recompute the article of recent declarations
from their composition and compare it with the `calculated_article` stored in the database.

Last result: 100 % parity on 300 declarations. Run it again after any change to article.py or to
Declaration.assign_calculated_article.
"""

from __future__ import annotations

from collections import Counter

from ..article import composition_from_declaration, compute_article
from ..config import Settings
from ..db import fetchall
from ..declarations import load_current
from ..refdata import RefData


def article_parity(settings: Settings, ref: RefData, n: int = 300, days: int = 45) -> dict:
    # Recently modified declarations only: older ones may have been computed with older reference data.
    rows = fetchall(
        settings,
        """select id from data_declaration
           where siccrf_id is null and calculated_article <> '' and status <> 'DRAFT'
             and modification_date > now() - (%s || ' days')::interval
           order by md5(id::text) limit %s""",
        (str(days), n),
    )
    ok, mismatches, pairs = 0, [], Counter()
    for r in rows:
        d = load_current(settings, r["id"])
        res = compute_article(composition_from_declaration(d, ref), ref)
        pairs[(d.calculated_article, res.article)] += 1
        if res.article == d.calculated_article:
            ok += 1
        else:
            mismatches.append(
                {
                    "declaration_id": d.declaration_id,
                    "stored": d.calculated_article,
                    "recomputed": res.article,
                    "reasons": res.reasons,
                }
            )
    total = len(rows)
    return {
        "n": total,
        "parity": round(ok / total, 4) if total else None,
        "confusion": {f"{a} -> {b}": c for (a, b), c in pairs.most_common()},
        "mismatches": mismatches[:50],
    }
