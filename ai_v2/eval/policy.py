"""OFFLINE simulation of decision policies, from the saved findings of a run (no model call).

Tries every combination of "families of MAJOR findings that block once confirmed by the agent",
two confirmation thresholds and two risk thresholds, then prints the Pareto frontier: for each
number of false positives, the simplest policy with the best recall. This is how the default
policy in config.Settings was chosen.

  python -m ai_v2.eval.policy <run_id> [--gold gold_v1.jsonl]
"""

from __future__ import annotations

import argparse
import itertools
import json

from ..config import Settings
from ..decision import decide
from ..schemas import Finding
from .gold_v1 import load_gold
from .metrics import _prf

# Families of finding codes that a policy can make blocking (when confirmed by the agent).
FAMILIES = {
    "mentions": ("R-MEN-", "R-DJR-DROPS-ML"),
    "warnings": ("R-WARN-",),
    "ingredients": ("R-ING-ACTIVE", "R-ING-MANY"),
    "doses": ("R-DOSE-HIGHER", "R-DJR-HIGHER"),
    "identity": ("R-ID-",),
    "claims": ("R-CLM-",),
}


def simulate(results: dict, gold: list, settings: Settings) -> dict:
    """Re-decide every saved result under `settings` and score it (+ block rate on the prod split)."""
    tp = fp = fn = tn = 0
    prod_block = prod_n = 0
    for g in gold:
        r = results.get(g.key)
        if not r or not r.get("findings") and (r.get("decision") or {}).get("decision") == "ERROR":
            continue
        findings = [Finding.model_validate(f) for f in r.get("findings", [])]
        prior = (r.get("triage") or {}).get("prior", 0.0)
        d = decide(findings, settings, r.get("name", ""), r.get("facts", {}), prior).decision == "BLOCK"
        if g.expected_block is True:
            tp += d
            fn += not d
        elif g.expected_block is False:
            fp += d
            tn += not d
        else:
            prod_n += 1
            prod_block += d
    m = _prf(tp, fp, fn, tn)
    m["prod_block_rate"] = round(prod_block / prod_n, 3) if prod_n else None
    return m


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("run_id")
    p.add_argument("--gold", default="gold_v1.jsonl")
    a = p.parse_args(argv)
    s = Settings()
    res = {}
    for f in (s.data_dir / "runs" / a.run_id / "results").glob("*.json"):
        r = json.loads(f.read_text(encoding="utf-8"))
        res[r["key"]] = r
    gold = [g for g in load_gold(s.data_dir / "gold" / a.gold) if g.key in res]
    adj_path = s.data_dir / "gold" / "adjudications_v1.json"
    if adj_path.exists():  # ground truth corrected after a visual check of the labels
        adj = {k: v for k, v in json.loads(adj_path.read_text(encoding="utf-8")).items() if not k.startswith("_")}
        gold = [
            g.model_copy(update={"expected_block": adj[g.key]["expected_block"]}) if g.key in adj else g for g in gold
        ]
        print(f"(adjudicated ground truth: {len(adj)} corrections)")
    rows = []
    names = list(FAMILIES)
    for k in range(0, len(names) + 1):
        for combo in itertools.combinations(names, k):
            for conf in (0.9, 0.95):
                for risk in (0.93, 0.97):
                    st = Settings()
                    st.confirmed_major_codes = tuple(c for n in combo for c in FAMILIES[n])
                    st.confirmed_major_confidence = conf
                    st.block_risk_score = risk
                    m = simulate(res, gold, st)
                    rows.append({"families": "+".join(combo) or "(none)", "conf": conf, "risk": risk, **m})
    # Pareto frontier: for each number of false positives, the simplest policy with the best recall
    best: dict[int, dict] = {}
    for r in sorted(rows, key=lambda r: (len(r["families"]), r["conf"])):
        cur = best.get(r["fp"])
        if cur is None or (r["recall"] or 0) > (cur["recall"] or 0):
            best[r["fp"]] = r
    print(f"{'families blocking when confirmed':<45} conf  risk  prec  recall  FP  FN  prod.block")
    for fp in sorted(best):
        r = best[fp]
        print(
            f"{r['families']:<45} {r['conf']:.2f} {r['risk']:.2f} "
            f"{(r['precision'] or 0):.2f}  {(r['recall'] or 0):.2f}  {r['fp']:>2}  {r['fn']:>2}  {r['prod_block_rate']}"
        )
    out = s.data_dir / "runs" / a.run_id / "policy_simulation.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(rows)} policies simulated -> {out}")


if __name__ == "__main__":
    main()
