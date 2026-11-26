"""Human-readable (Markdown) report of a run, written to runs/<run_id>/report.md."""

from __future__ import annotations

from .gold_v1 import GoldEntry


def _pct(x):
    return "n/a" if x is None else f"{100 * x:.0f} %"


def render_report(run_id: str, metrics: dict, gold: list[GoldEntry], results: dict[str, dict], usage: dict) -> str:
    e = metrics["end_to_end"]
    a15 = metrics["end_to_end_art15"]
    L = [
        f"# Run {run_id}",
        "",
        "## End-to-end result (instructor positives vs negatives validated by a human)",
        "",
        f"- Evaluated: {metrics['n_labelled_evaluated']} (errors: {len(metrics['errors'])})",
        f"- **Block precision: {_pct(e['precision'])}** (share of blocked declarations that really had a problem)",
        f"- **Recall: {_pct(e['recall'])}** (share of problematic declarations that were blocked)",
        f"- TP {e['tp']} · FP {e['fp']} · FN {e['fn']} · TN {e['tn']}",
        f"- Article 15 scope only (the scope of automatic validation): precision {_pct(a15['precision'])}, "
        f"recall {_pct(a15['recall'])} (TP {a15['tp']} · FP {a15['fp']} · FN {a15['fn']} · TN {a15['tn']})",
        *(
            [
                f"- **After visual adjudication of {metrics['adjudicated']['n_adjudications']} cases** "
                f"(`gold/adjudications_v1.json`): precision {_pct(metrics['adjudicated']['end_to_end']['precision'])}, "
                f"recall {_pct(metrics['adjudicated']['end_to_end']['recall'])}; article 15 scope: precision "
                f"{_pct(metrics['adjudicated']['end_to_end_art15']['precision'])}, recall "
                f"{_pct(metrics['adjudicated']['end_to_end_art15']['recall'])}"
            ]
            if metrics.get("adjudicated")
            else []
        ),
        f"- Precision@k (ranking by risk score): {metrics['precision_at_k']}",
        f"- Recommended risk score threshold for a precision >= 95 %: {metrics['recommended_risk_threshold']}",
        "",
        "## Detection by issue type (positives)",
        "",
        "| Category (instructor comment) | n | detected | detected and blocked |",
        "|---|---|---|---|",
    ]
    for cat, d in sorted(metrics["per_category"].items(), key=lambda x: -x[1]["n"]):
        L.append(f"| {cat} | {d['n']} | {_pct(d['detection_rate'])} | {_pct(d['blocked_rate'])} |")
    p = metrics["prod_sample"]
    q = metrics["reading_quality_on_negatives"]
    L += [
        "",
        "## Production sample (automatically validated article 15 declarations, unknown truth)",
        "",
        f"- {p['blocked']} blocked out of {p['n']} ({_pct(p['block_rate'])}). Reasons: {p['reasons']}",
        "",
        "## Reading and matching quality (negatives)",
        "",
        f"- Share of declared actives found on the label: {_pct(q['declared_active_coverage_mean'])}",
        f"- Share of label ingredients not matched to the declaration: {_pct(q['label_ingredients_unmatched_share_mean'])}",
        "",
        "## Reasons of false positives / true positives",
        "",
        f"- FP: {metrics['false_positive_reasons']}",
        f"- TP: {metrics['true_positive_reasons']}",
        "",
        "## Cost and speed",
        "",
        f"- Estimated total cost: {usage.get('total_cost_usd')} $, i.e. {metrics['cost_usd']['mean_per_declaration']} $ per declaration",
        f"- Latency per declaration: mean {metrics['latency_s']['mean']} s, median {metrics['latency_s']['median']} s",
        "",
        "| Stage | calls | cost $ | tokens in | tokens out | pages |",
        "|---|---|---|---|---|---|",
    ]
    for st, d in sorted(usage.get("by_stage", {}).items(), key=lambda x: -x[1]["cost_usd"]):
        L.append(
            f"| {st} | {d['calls']} | {d['cost_usd']:.3f} | {d['input_tokens']} | {d['output_tokens']} | {d['pages']} |"
        )
    L += [
        "",
        "## Per declaration",
        "",
        "| key | split | expected | decision | risk | reasons | cost $ |",
        "|---|---|---|---|---|---|---|",
    ]
    for g in gold:
        r = results.get(g.key)
        if not r:
            continue
        d = r.get("decision") or {}
        exp = {True: "BLOCK", False: "PASS", None: "?"}[g.expected_block]
        L.append(
            f"| {g.key} | {g.split} | {exp} | {d.get('decision')} | {d.get('risk_score')} | "
            f"{', '.join(d.get('reason_codes') or [])[:120]} | {r.get('cost_usd')} |"
        )
    return "\n".join(L) + "\n"
