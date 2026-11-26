"""Run storage: EVERYTHING is saved, so that any run can be read, compared and re-evaluated later.

ai_v2_data/runs/
  index.jsonl                      one line per run (date, name, key metrics)
  <run_id>/
    manifest.json                  full config, models, prompt versions, reference data, git commit, dataset
    results/<key>.json             full trace per declaration (extraction, resolution, findings,
                                   agent verification, decision, message, cost, latency)
    results.jsonl                  one summary line per declaration
    metrics.json / report.md       evaluation against the gold set
    usage.json                     cost and tokens per stage
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

from .config import Settings


def _git_commit() -> str | None:
    """Short hash of the checked-out commit, recorded in the manifest (None outside a git checkout)."""
    try:
        return (
            subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
                timeout=10,
            ).stdout.strip()
            or None
        )
    except Exception:  # noqa: BLE001
        return None


class RunStore:
    def __init__(self, settings: Settings, name: str, run_dir: Path | None = None):
        """New run (`run_dir` None: the id is a timestamp + `name`), or an existing run to re-open."""
        self.root = settings.data_dir / "runs"
        self.root.mkdir(parents=True, exist_ok=True)
        if run_dir is None:
            safe = re.sub(r"[^A-Za-z0-9_-]+", "-", name)[:40]
            self.run_id = f"{time.strftime('%Y%m%d-%H%M%S')}_{safe}"
            self.dir = self.root / self.run_id
        else:
            self.dir, self.run_id = run_dir, run_dir.name
        (self.dir / "results").mkdir(parents=True, exist_ok=True)

    def write_manifest(self, manifest: dict) -> None:
        manifest = {
            "run_id": self.run_id,
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "git_commit": _git_commit(),
            **manifest,
        }
        (self.dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )

    def save_result(self, result: dict) -> None:
        """Write the full trace of one declaration, and append its summary line to results.jsonl."""
        key = re.sub(r"[^A-Za-z0-9_-]+", "_", result["key"])
        (self.dir / "results" / f"{key}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8"
        )
        d = result.get("decision") or {}
        line = {
            "key": result["key"],
            "declaration_id": result.get("declaration_id"),
            "decision": d.get("decision"),
            "risk": d.get("risk_score"),
            "reasons": d.get("reason_codes"),
            "cost_usd": result.get("cost_usd"),
            "latency_s": result.get("latency_s"),
            "error": result.get("error"),
        }
        with (self.dir / "results.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    def finalize(self, metrics: dict, report_md: str, usage: dict, extra: dict | None = None) -> None:
        """Write metrics, report and usage, and add the run to runs/index.jsonl."""
        (self.dir / "metrics.json").write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        (self.dir / "report.md").write_text(report_md, encoding="utf-8")
        (self.dir / "usage.json").write_text(json.dumps(usage, ensure_ascii=False, indent=2), encoding="utf-8")
        e2e = metrics.get("end_to_end", {})
        line = {
            "run_id": self.run_id,
            "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "precision": e2e.get("precision"),
            "recall": e2e.get("recall"),
            "f1": e2e.get("f1"),
            "prod_block_rate": metrics.get("prod_sample", {}).get("block_rate"),
            "cost_usd": usage.get("total_cost_usd"),
            **(extra or {}),
        }
        with (self.root / "index.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False, default=str) + "\n")

    def load_results(self) -> dict[str, dict]:
        """All the per-declaration results of the run, by key."""
        out = {}
        for p in sorted((self.dir / "results").glob("*.json")):
            r = json.loads(p.read_text(encoding="utf-8"))
            out[r["key"]] = r
        return out
