"""Content-addressed cache, one namespace per pipeline stage.

Key = stage + hash(model, prompt version, schema, input...). Changing the resolution prompt
re-runs neither the OCR nor the extraction, and re-running an identical run costs nothing.
Storage is a single local SQLite file, safe across threads thanks to a lock.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any


def stable_hash(obj: Any) -> str:
    """sha256 of a canonical JSON dump: the same content always gives the same hash (key order ignored)."""
    data = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


class Cache:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(path), check_same_thread=False, timeout=60)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, stage TEXT, created REAL, value TEXT)"
        )
        self._conn.execute("CREATE INDEX IF NOT EXISTS cache_stage ON cache(stage)")
        self._conn.commit()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def key(stage: str, **parts: Any) -> str:
        # The stage stays readable at the start of the key (used for per-stage stats and purges).
        return f"{stage}:{stable_hash(parts)}"

    def get(self, key: str) -> Any | None:
        with self._lock:
            row = self._conn.execute("SELECT value FROM cache WHERE key=?", (key,)).fetchone()
        if row is None:
            self.misses += 1
            return None
        self.hits += 1
        return json.loads(row[0])

    def set(self, key: str, value: Any) -> None:
        stage = key.split(":", 1)[0]
        payload = json.dumps(value, ensure_ascii=False, default=str)
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO cache (key, stage, created, value) VALUES (?,?,?,?)",
                (key, stage, time.time(), payload),
            )
            self._conn.commit()

    def stats(self) -> dict:
        with self._lock:
            rows = self._conn.execute("SELECT stage, count(*) FROM cache GROUP BY stage").fetchall()
        return {"hits": self.hits, "misses": self.misses, "entries_by_stage": dict(rows)}
