"""Command line.

python -m ai_v2.cli refdata [--refresh]          freeze the reference data (read-only)
python -m ai_v2.cli parity [--n 300]             parity of the article calculation with the app
python -m ai_v2.cli gold-build                   build gold set v1 (from instructor decisions)
python -m ai_v2.cli gold-import FILE             import the hand-annotated dataset (v2)
python -m ai_v2.cli run --gold FILE [...]        run a test series, save everything
python -m ai_v2.cli run-ids 123,456              analyse declarations (current state)
python -m ai_v2.cli reeval RUN_ID --gold F       recompute a run's metrics and report
python -m ai_v2.cli runs                         list the runs
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time

from .config import Settings
from .db import run_db
from .declarations import load_current, load_snapshot


def _settings(args) -> Settings:
    """Settings with the command-line overrides applied."""
    s = Settings()
    if getattr(args, "budget", None):
        s.budget_usd = args.budget
    if getattr(args, "no_agent", False):
        s.agent_enabled = False
    if getattr(args, "concurrency", None):
        s.max_concurrent_declarations = args.concurrency
    return s


async def _load_decls(settings, entries):
    """Load the declarations of gold entries: snapshot state for "snap:" keys, current state otherwise."""

    async def one(e):
        try:
            if e.key.startswith("snap:"):
                return await run_db(load_snapshot, settings, e.snapshot_id)
            return await run_db(load_current, settings, e.declaration_id)
        except Exception as ex:  # noqa: BLE001
            print(f"  ! cannot load {e.key}: {ex}", file=sys.stderr)
            return None

    return [d for d in await asyncio.gather(*(one(e) for e in entries)) if d]


def _adjudicated_metrics(s: Settings, gold, results, metrics: dict) -> None:
    """Add metrics computed on the adjudicated ground truth (gold/adjudications_v1.json), if present."""
    from .eval.metrics import evaluate

    adj_path = s.data_dir / "gold" / "adjudications_v1.json"
    if adj_path.exists():
        adj = {k: v for k, v in json.loads(adj_path.read_text(encoding="utf-8")).items() if not k.startswith("_")}
        m_adj = evaluate(gold, results, adjudications=adj)
        metrics["adjudicated"] = {
            "n_adjudications": len(adj),
            "end_to_end": m_adj["end_to_end"],
            "end_to_end_art15": m_adj["end_to_end_art15"],
        }


async def cmd_run(args) -> None:
    """Run the pipeline on a gold set, save every result as it comes, then evaluate."""
    from .eval.gold_v1 import load_gold
    from .eval.metrics import evaluate
    from .eval.report import render_report
    from .pipeline import Pipeline
    from .refdata import load_refdata
    from .runs import RunStore

    s = _settings(args)
    # A bare file name is looked up in <data_dir>/gold/.
    gold_path = s.data_dir / "gold" / args.gold if "/" not in args.gold and "\\" not in args.gold else args.gold
    gold = load_gold(gold_path)
    if args.splits:
        gold = [g for g in gold if g.split in args.splits.split(",")]
    if args.limit:
        gold = gold[: args.limit]
    ref = load_refdata(s)
    store = RunStore(s, args.name or "run")
    store.write_manifest(
        {
            "gold": str(gold_path),
            "n": len(gold),
            "splits": args.splits,
            "settings": s.public_dict(),
            "refdata_version": ref.version,
            "keys": [g.key for g in gold],
        }
    )
    print(f"Run {store.run_id}: {len(gold)} declarations -> {store.dir}")
    t0 = time.monotonic()
    decls = await _load_decls(s, gold)
    print(f"  {len(decls)} declarations loaded in {time.monotonic() - t0:.0f}s")
    # No leakage: the agent never sees the instructor comments of the declarations under evaluation
    pipe = Pipeline(s, exclude_from_doctrine={g.declaration_id for g in load_gold(gold_path)})
    done = {"n": 0}

    def on_result(r):
        done["n"] += 1
        store.save_result(r)
        d = r.get("decision") or {}
        print(
            f"  [{done['n']:>3}/{len(decls)}] {r['key']:<14} {d.get('decision'):<6} risk={d.get('risk_score')} "
            f"cost={r.get('cost_usd')}$ {r.get('latency_s')}s {','.join(d.get('reason_codes') or [])[:90]}"
            + (f" ERROR {r.get('error', '')[:120]}" if d.get("decision") == "ERROR" else ""),
            flush=True,
        )

    try:
        await pipe.run_many(decls, on_result)
    finally:
        await pipe.aclose()
    results = store.load_results()
    metrics = evaluate(gold, results)
    _adjudicated_metrics(s, gold, results, metrics)
    metrics["cache"] = pipe.cache.stats()
    metrics["wall_clock_s"] = round(time.monotonic() - t0, 1)
    usage = pipe.usage.summary()
    store.finalize(metrics, render_report(store.run_id, metrics, gold, results, usage), usage, {"name": args.name})
    print(
        json.dumps(
            {
                k: metrics[k]
                for k in ("end_to_end", "precision_at_k", "prod_sample", "cost_usd", "latency_s", "wall_clock_s")
            },
            ensure_ascii=False,
            indent=1,
            default=str,
        )
    )
    print(f"Report: {store.dir / 'report.md'}")


async def cmd_run_ids(args) -> None:
    """Analyse ad-hoc declarations (current state): writes a temporary gold file, then runs it."""
    from .eval.gold_v1 import GoldEntry, save_gold

    ids = [int(x) for x in args.ids.split(",") if x.strip()]
    entries = [GoldEntry(key=f"decl:{i}", split="adhoc", snapshot_id=0, declaration_id=i) for i in ids]
    s = _settings(args)
    path = s.data_dir / "gold" / f"adhoc_{time.strftime('%Y%m%d-%H%M%S')}.jsonl"
    save_gold(entries, path)
    args.gold, args.splits, args.limit = str(path), None, None
    await cmd_run(args)


async def cmd_gold_build(args) -> None:
    from .cache import Cache
    from .eval.gold_v1 import build_gold_v1, save_gold
    from .llm import LLMClient, Usage

    s = _settings(args)
    cache = Cache(s.data_dir / "cache" / "cache.sqlite")
    client = LLMClient(s, cache, Usage(s.budget_usd))
    try:
        g = await build_gold_v1(client, s, args.pos, args.neg, args.prod, seed=args.seed)
    finally:
        await client.aclose()
    path = s.data_dir / "gold" / args.out
    save_gold(g, path)
    print(f"{len(g)} entries -> {path}")


def cmd_reeval(args) -> None:
    """Recompute the metrics and report of an existing run. With --redecide, first re-apply the
    CURRENT decision policy to the saved findings (no model call): this is how a policy change is tested."""
    from .eval.gold_v1 import load_gold
    from .eval.metrics import evaluate
    from .eval.report import render_report
    from .runs import RunStore

    s = Settings()
    store = RunStore(s, "", run_dir=s.data_dir / "runs" / args.run_id)
    gold = load_gold(s.data_dir / "gold" / args.gold if "/" not in args.gold else args.gold)
    results = store.load_results()
    gold = [g for g in gold if g.key in results]
    if args.redecide:
        from .decision import decide
        from .schemas import Finding

        for r in results.values():
            if (r.get("decision") or {}).get("decision") == "ERROR":
                continue
            r.setdefault("decision_at_run", r["decision"])  # keep the original decision for comparison
            findings = [Finding.model_validate(f) for f in r.get("findings", [])]
            r["decision"] = decide(
                findings, s, r.get("name", ""), r.get("facts", {}), (r.get("triage") or {}).get("prior", 0.0)
            ).model_dump()
            r["policy"] = {
                "confirmed_major_codes": s.confirmed_major_codes,
                "confirmed_major_confidence": s.confirmed_major_confidence,
                "block_confidence": s.block_confidence,
                "block_risk_score": s.block_risk_score,
            }
            store.save_result(r)
    metrics = evaluate(gold, results)
    _adjudicated_metrics(s, gold, results, metrics)
    usage = (
        json.loads((store.dir / "usage.json").read_text(encoding="utf-8"))
        if (store.dir / "usage.json").exists()
        else {}
    )
    (store.dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (store.dir / "report.md").write_text(render_report(store.run_id, metrics, gold, results, usage), encoding="utf-8")
    print(json.dumps(metrics["end_to_end"], indent=1))


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="ai_v2")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("refdata", help="freeze the reference data")
    a.add_argument("--refresh", action="store_true", help="reload from the database even if a recent snapshot exists")
    a = sub.add_parser("parity", help="parity of the article calculation with the app")
    a.add_argument("--n", type=int, default=300)
    a = sub.add_parser("gold-build", help="build gold set v1 from instructor decisions")
    a.add_argument("--pos", type=int, default=50)
    a.add_argument("--neg", type=int, default=30)
    a.add_argument("--prod", type=int, default=20)
    a.add_argument("--seed", type=int, default=42)
    a.add_argument("--out", default="gold_v1.jsonl")
    a = sub.add_parser("gold-import", help="import a hand-annotated dataset (see eval/gold_v2.py)")
    a.add_argument("file")
    a.add_argument("--out", default="gold_v2.jsonl")
    for name in ("run", "run-ids"):
        a = sub.add_parser(name)
        if name == "run":
            a.add_argument("--gold", required=True, help="gold file (bare name: looked up in <data_dir>/gold/)")
            a.add_argument("--splits", help="comma-separated splits to keep (positive,negative,prod)")
            a.add_argument("--limit", type=int)
        else:
            a.add_argument("ids", help="comma-separated declaration ids")
        a.add_argument("--name")
        a.add_argument("--budget", type=float, help="max estimated spend in USD")
        a.add_argument("--no-agent", action="store_true")
        a.add_argument("--concurrency", type=int)
    a = sub.add_parser("reeval", help="recompute a run's metrics and report")
    a.add_argument("run_id")
    a.add_argument("--gold", required=True)
    a.add_argument("--redecide", action="store_true", help="re-apply the current decision policy")
    sub.add_parser("runs", help="list the runs")
    args = p.parse_args(argv)

    if args.cmd == "refdata":
        from .refdata import load_refdata

        ref = load_refdata(Settings(), refresh=args.refresh)
        print(f"reference data {ref.version}: {len(ref.elements)} elements")
    elif args.cmd == "parity":
        from .eval.parity import article_parity
        from .refdata import load_refdata

        s = Settings()
        print(json.dumps(article_parity(s, load_refdata(s), n=args.n), ensure_ascii=False, indent=1))
    elif args.cmd == "gold-build":
        asyncio.run(cmd_gold_build(args))
    elif args.cmd == "gold-import":
        from pathlib import Path

        from .eval.gold_v1 import save_gold
        from .eval.gold_v2 import import_gold_v2

        s = Settings()
        g = import_gold_v2(Path(args.file))
        save_gold(g, s.data_dir / "gold" / args.out)
        print(f"{len(g)} entries imported -> {s.data_dir / 'gold' / args.out}")
    elif args.cmd == "run":
        asyncio.run(cmd_run(args))
    elif args.cmd == "run-ids":
        asyncio.run(cmd_run_ids(args))
    elif args.cmd == "reeval":
        cmd_reeval(args)
    elif args.cmd == "runs":
        idx = Settings().data_dir / "runs" / "index.jsonl"
        print(idx.read_text(encoding="utf-8") if idx.exists() else "no run yet")


if __name__ == "__main__":
    main()
