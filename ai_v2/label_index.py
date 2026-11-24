"""Index of label files across declarations: perceptual fingerprint (dHash) AND text fingerprint.

"Fake label" signal: the SAME label attached to declarations of different products (seen in
production: one English-language label attached to three unrelated, auto-validated declarations).

The image alone is not enough: labels of one product range share a graphic template and get
the same low-resolution fingerprint. We therefore also require a near-identical text. The same
product declared again (similar name) is not reported. In production, the index must be
pre-filled with the history (download, rendering and OCR, no LLM call).
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from rapidfuzz import fuzz

from .text import normalise

MAX_HAMMING = 4  # max differing bits (out of 64) between two dHashes of the same artwork
MIN_TEXT_SIMILARITY = 92  # min fuzz.ratio between the two label texts


def hamming(a: str, b: str) -> int:
    return bin(int(a, 16) ^ int(b, 16)).count("1")


class LabelIndex:
    def __init__(self, path: Path):
        self.path = path
        self._lock = threading.Lock()
        self.entries: list[dict] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []

    def check_and_add(self, decl, docs, text: str = "") -> list[dict]:
        """Return the entries of OTHER products whose label matches this one, then index this label."""
        # blank or uniform pages give a degenerate hash (all 0 or all f): ignored
        hashes = [p.dhash for d in docs for p in d.pages if p.dhash and p.dhash.strip("0f")]
        text_fp = normalise(text)[:6000]
        found: dict[int, dict] = {}
        with self._lock:
            for e in self.entries:
                if e["declaration_id"] == decl.declaration_id:
                    continue
                if not any(hamming(h, e["dhash"]) <= MAX_HAMMING for h in hashes):
                    continue
                if text_fp and e.get("text") and fuzz.ratio(text_fp, e["text"]) < MIN_TEXT_SIMILARITY:
                    continue  # same graphic template, different content: not a reuse
                if fuzz.token_set_ratio(normalise(e["name"]), normalise(decl.name)) >= 80:
                    continue  # same product (declared again)
                found[e["declaration_id"]] = e
            known = {(e["declaration_id"], e["dhash"]) for e in self.entries}
            for h in hashes:
                if (decl.declaration_id, h) not in known:
                    self.entries.append(
                        {
                            "declaration_id": decl.declaration_id,
                            "name": decl.name,
                            "dhash": h,
                            "company_id": decl.company_id,
                            "text": text_fp,
                        }
                    )
        return list(found.values())

    def save(self) -> None:
        with self._lock:
            self.path.write_text(json.dumps(self.entries, ensure_ascii=False), encoding="utf-8")
