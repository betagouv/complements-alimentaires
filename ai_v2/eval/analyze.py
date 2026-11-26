"""Error analysis of a run: false positives, false negatives, findings refuted by the agent.

python -m ai_v2.eval.analyze <run_id> [--gold gold_v1.jsonl] [--show 12]
"""

from __future__ import annotations

import argparse
import json
from collections import Counter

from ..config import Settings
from .gold_v1 import load_gold


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("run_id")
    p.add_argument("--gold", default="gold_v1.jsonl")
    p.add_argument("--show", type=int, default=12, help="number of cases to print per section")
    a = p.parse_args(argv)
    s = Settings()
    run_dir = s.data_dir / "runs" / a.run_id
    res = {}
    for f in (run_dir / "results").glob("*.json"):
        r = json.loads(f.read_text(encoding="utf-8"))
        res[r["key"]] = r
    gold = {g.key: g for g in load_gold(s.data_dir / "gold" / a.gold)}
    fps, fns, refuted, confirmed = [], [], Counter(), Counter()
    for k, r in res.items():
        g = gold.get(k)
        dec = (r.get("decision") or {}).get("decision")
        for f in r.get("findings", []):
            if f.get("verified") == "refuted":
                refuted[f["code"]] += 1
            elif f.get("verified") == "confirmed":
                confirmed[f["code"]] += 1
        if not g or g.expected_block is None:
            continue
        if g.expected_block is False and dec == "BLOCK":
            fps.append((g, r))
        if g.expected_block is True and dec == "PASS":
            fns.append((g, r))
    print(f"{len(res)} results | FP {len(fps)} | FN {len(fns)}")
    print("refuted by the agent:", refuted.most_common(12))
    print("confirmed by the agent:", confirmed.most_common(12))
    print("\n================ FALSE POSITIVES")
    for g, r in fps[: a.show]:
        print(f"--- {g.key} risk={r['decision']['risk_score']} reasons={r['decision']['reason_codes']}")
        for f in r["findings"]:
            if f["id"] in r["decision"]["blocking_findings"] or f["severity"] in ("BLOCKING", "MAJOR"):
                print(
                    f"   {f['severity']} {f['code']} c={f['confidence']} v={f.get('verified')} | {f['detail'][:220]}"
                )
                if f.get("verification_note"):
                    print(f"      agent: {f['verification_note'][:220]}")
    print("\n================ FALSE NEGATIVES")
    for g, r in fns[: a.show]:
        cats = [i.category.value for i in (g.structured.issues if g.structured else [])]
        print(f"--- {g.key} risk={r['decision']['risk_score']} expected={cats}")
        print(f"   instructor: {g.comment[:300]}")
        for f in r.get("findings", []):
            if f["severity"] in ("BLOCKING", "MAJOR"):
                print(f"   {f['severity']} {f['code']} c={f['confidence']} v={f.get('verified')} | {f['title'][:120]}")
        if r.get("error"):
            print("   ERROR", r["error"][:200])


if __name__ == "__main__":
    main()
