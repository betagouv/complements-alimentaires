"""Evaluation metrics: end to end (block / let through), per fraud type, per stage (reading +
matching), risk threshold calibration, cost and latency.

Vocabulary: a "positive" is a declaration that should be blocked. Precision = share of blocked
declarations that really had a problem (what matters most, since nobody reviews the blocks);
recall = share of problematic declarations that were blocked.
"""

from __future__ import annotations

from collections import Counter
from statistics import mean, median

from .gold_v1 import GoldEntry

# Issue category (instructor comment) -> finding code prefixes that "cover" it
CATEGORY_TO_CODES = {
    "undeclared_ingredient": ("R-ING", "R-ART"),
    "missing_mention": ("R-MEN",),
    "missing_specific_warning": ("R-WARN",),
    "quantities_missing_on_label": ("R-MEN-quantities_per_daily_dose",),
    "dose_inconsistency": ("R-DOSE", "R-DJR"),
    "dose_over_max": ("R-DOSE-OVERMAX", "R-ART-BYPASS", "R-DOSE-HIGHER"),
    "label_other_product": ("R-ID", "R-ING-MASSIVE", "R-DOC"),
    "djr_or_galenic_inconsistency": ("R-DJR", "R-ID"),
    "claims": ("R-CLM",),
    "other_label": ("R-",),
}


def _prf(tp, fp, fn, tn) -> dict:
    """Precision, recall, F1 and accuracy from a confusion matrix (None when undefined)."""
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f1 = 2 * p * r / (p + r) if p and r else None
    acc = (tp + tn) / (tp + fp + fn + tn) if tp + fp + fn + tn else None
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": p, "recall": r, "f1": f1, "accuracy": acc}


def evaluate(
    gold: list[GoldEntry], results: dict[str, dict], target_precision: float = 0.95, adjudications: dict | None = None
) -> dict:
    """Compare run results with the gold set.

    adjudications: {key: {"expected_block": bool, "note": str}}, corrections of the ground truth
    after a visual check of the label. When given, metrics are computed on the adjudicated truth.
    ERROR results are excluded from the confusion matrix and listed in "errors".
    """
    if adjudications:
        gold = [
            g.model_copy(update={"expected_block": adjudications[g.key]["expected_block"]})
            if g.key in adjudications and g.expected_block is not None
            else g
            for g in gold
        ]
    labelled = [g for g in gold if g.expected_block is not None and g.key in results]
    ok = [g for g in labelled if results[g.key].get("decision", {}).get("decision") in ("BLOCK", "PASS")]
    errors = [
        g.key for g in gold if g.key in results and results[g.key].get("decision", {}).get("decision") == "ERROR"
    ]

    def blocked(g):
        return results[g.key]["decision"]["decision"] == "BLOCK"

    tp = sum(1 for g in ok if g.expected_block and blocked(g))
    fp = sum(1 for g in ok if not g.expected_block and blocked(g))
    fn = sum(1 for g in ok if g.expected_block and not blocked(g))
    tn = sum(1 for g in ok if not g.expected_block and not blocked(g))
    end_to_end = _prf(tp, fp, fn, tn)
    # Real scope of automatic blocking: article 15 declarations (the others always go to an instructor)
    art15 = [g for g in ok if (g.article or "").startswith("ART_15")]
    end_to_end_art15 = _prf(
        sum(1 for g in art15 if g.expected_block and blocked(g)),
        sum(1 for g in art15 if not g.expected_block and blocked(g)),
        sum(1 for g in art15 if g.expected_block and not blocked(g)),
        sum(1 for g in art15 if not g.expected_block and not blocked(g)),
    )

    # Recall per category: blocked AND at least one finding of the right family
    per_cat: dict[str, dict] = {}
    for g in ok:
        if not g.expected_block or not g.structured:
            continue
        codes = [f["code"] for f in results[g.key].get("findings", []) if f.get("verified") != "refuted"]
        for cat in {i.category.value for i in g.structured.issues if i.category.value != "not_label"}:
            prefixes = CATEGORY_TO_CODES.get(cat, ("R-",))
            hit = any(c.startswith(prefixes) for c in codes)
            d = per_cat.setdefault(cat, {"n": 0, "detected": 0, "detected_and_blocked": 0})
            d["n"] += 1
            d["detected"] += hit
            d["detected_and_blocked"] += hit and blocked(g)
    for d in per_cat.values():
        d["detection_rate"] = round(d["detected"] / d["n"], 3)
        d["blocked_rate"] = round(d["detected_and_blocked"] / d["n"], 3)

    # Threshold curve on the risk score (calibration) + precision@k (ranking quality)
    scored = sorted(
        ((results[g.key]["decision"].get("risk_score") or 0.0, g.expected_block) for g in ok), reverse=True
    )
    curve = []
    for thr in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.93, 0.95, 0.97, 0.99]:
        tp_ = sum(1 for s, y in scored if s >= thr and y)
        fp_ = sum(1 for s, y in scored if s >= thr and not y)
        fn_ = sum(1 for s, y in scored if s < thr and y)
        tn_ = sum(1 for s, y in scored if s < thr and not y)
        m = _prf(tp_, fp_, fn_, tn_)
        curve.append({"threshold": thr, "precision": m["precision"], "recall": m["recall"], "fp": fp_, "tp": tp_})
    feasible = [c for c in curve if c["precision"] is not None and c["precision"] >= target_precision]
    best = max(feasible, key=lambda c: (c["recall"] or 0)) if feasible else None
    p_at_k = {}
    for k in (10, 20, 30):
        top = scored[:k]
        if top:
            p_at_k[f"p@{k}"] = round(sum(1 for _, y in top if y) / len(top), 3)

    # Reading + matching quality on the NEGATIVES (a human judged the label compliant)
    neg = [results[g.key] for g in ok if g.expected_block is False]
    coverage = [
        r.get("facts", {}).get("declared_active_coverage")
        for r in neg
        if r.get("facts", {}).get("declared_active_coverage") is not None
    ]
    unmatched_share = [
        r["facts"]["label_ingredients_unmatched"] / r["facts"]["label_ingredients"]
        for r in neg
        if r.get("facts", {}).get("label_ingredients")
    ]

    # Prod (unknown truth): block rate and reasons
    prod = [results[g.key] for g in gold if g.split == "prod" and g.key in results]
    prod_block = [r for r in prod if r.get("decision", {}).get("decision") == "BLOCK"]

    all_res = [results[g.key] for g in gold if g.key in results]
    costs = [r.get("cost_usd", 0) for r in all_res if r.get("cost_usd") is not None]
    lat = [r.get("latency_s", 0) for r in all_res if r.get("latency_s") is not None]
    fp_codes = Counter(
        c for g in ok if not g.expected_block and blocked(g) for c in results[g.key]["decision"]["reason_codes"]
    )
    tp_codes = Counter(
        c for g in ok if g.expected_block and blocked(g) for c in results[g.key]["decision"]["reason_codes"]
    )
    return {
        "n_gold": len(gold),
        "n_labelled_evaluated": len(ok),
        "errors": errors,
        "end_to_end": end_to_end,
        "end_to_end_art15": end_to_end_art15,
        "per_category": per_cat,
        "threshold_curve": curve,
        "recommended_risk_threshold": best,
        "precision_at_k": p_at_k,
        "reading_quality_on_negatives": {
            "declared_active_coverage_mean": round(mean(coverage), 3) if coverage else None,
            "label_ingredients_unmatched_share_mean": round(mean(unmatched_share), 3) if unmatched_share else None,
        },
        "prod_sample": {
            "n": len(prod),
            "blocked": len(prod_block),
            "block_rate": round(len(prod_block) / len(prod), 3) if prod else None,
            "reasons": Counter(c for r in prod_block for c in r["decision"]["reason_codes"]).most_common(10),
        },
        "false_positive_reasons": fp_codes.most_common(10),
        "true_positive_reasons": tp_codes.most_common(10),
        "cost_usd": {"total": round(sum(costs), 4), "mean_per_declaration": round(mean(costs), 4) if costs else None},
        "latency_s": {"mean": round(mean(lat), 1) if lat else None, "median": round(median(lat), 1) if lat else None},
    }
