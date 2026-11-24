"""Text normalisation and fuzzy quote search (used to "ground" every piece of evidence)."""

from __future__ import annotations

import re

from rapidfuzz import fuzz
from unidecode import unidecode

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normalise(text: str | None) -> str:
    """Lower-case, strip accents, keep only letters and digits separated by single spaces.

    All regexes in rules.py are written against this normalised form (no accents, no punctuation).
    """
    return " ".join(_NON_ALNUM.sub(" ", unidecode(text or "").lower()).split())


def quote_in_text(quote: str | None, text: str, threshold: float = 85.0) -> float:
    """Score 0-100 for the presence of a quote in a text (tolerates OCR errors, case and accents)."""
    q = normalise(quote)
    if not q:
        return 0.0
    t = normalise(text)
    if q in t:
        return 100.0
    if len(q) < 4:  # too short for a fuzzy match to mean anything
        return 0.0
    return float(fuzz.partial_ratio(q, t))


def contains_any(text: str, patterns: list[str]) -> str | None:
    """Return the first pattern (regex on the normalised text) found in `text`, else None."""
    t = normalise(text)
    for p in patterns:
        m = re.search(p, t)
        if m:
            return m.group(0)
    return None


# E-numbers of additives: "E 330", "E-464", "e160a"...
E_NUMBER = re.compile(r"\be\s?-?\s?(\d{3,4})\s?([a-z])?\b")


def e_numbers(text: str | None) -> list[str]:
    """E-numbers found in a text, in canonical form ("E330", "E160a")."""
    out = []
    for m in E_NUMBER.finditer(normalise(text)):
        out.append(f"E{m.group(1)}{(m.group(2) or '').lower()}")
    return out
