"""Unit conversion, to compare quantities read on the label with the declaration and the max doses."""

from __future__ import annotations

import re

from .text import normalise

# Masses, expressed in micrograms.
MASS_UG = {"kg": 1e9, "g": 1e6, "mg": 1e3, "ug": 1.0, "ng": 1e-3}
# Spellings found on labels (French and English) -> canonical unit.
UNIT_ALIASES = {
    "µg": "ug", "μg": "ug", "mcg": "ug", "ug": "ug", "microgramme": "ug", "microgrammes": "ug",
    "mg": "mg", "milligramme": "mg", "milligrammes": "mg",
    "g": "g", "gramme": "g", "grammes": "g", "gr": "g",
    "kg": "kg", "ng": "ng",
    "ml": "ml", "millilitre": "ml", "millilitres": "ml", "cl": "cl", "l": "l",
    "ui": "ui", "iu": "ui", "u i": "ui",
    "ufc": "ufc", "cfu": "ufc", "ufc/j": "ufc",
    "%": "%",
}  # fmt: skip
# Multiplier words, mostly for probiotics ("10 milliards UFC").
MULTIPLIERS = {
    "milliard": 1e9,
    "milliards": 1e9,
    "md": 1e9,
    "billion": 1e9,
    "billions": 1e9,
    "million": 1e6,
    "millions": 1e6,
}

# International units -> µg (usual regulatory values). Keys are matched against the normalised substance name.
UI_TO_UG = {
    "vitamine d": 1 / 40,  # 1 µg = 40 IU
    "vitamine a": 0.3,  # 1 IU retinol = 0.3 µg
    "vitamine e": 1000 / 1.49,  # 1 IU = 0.67 mg d-alpha-tocopherol (low, conservative bound)
}


def canonical_unit(unit: str | None) -> tuple[str | None, float]:
    """Return (canonical unit, multiplier), e.g. 'milliards UFC' -> ('ufc', 1e9). Unknown unit -> None."""
    if not unit:
        return None, 1.0
    u = unit.strip().lower().replace("μ", "µ")
    mult = 1.0
    for word, m in MULTIPLIERS.items():
        if re.search(rf"\b{word}\b", u):
            mult = m
            u = re.sub(rf"\b{word}\b", "", u).strip()
    u = u.replace("de ", "").replace("d'", "").strip()
    if u in UNIT_ALIASES:
        return UNIT_ALIASES[u], mult
    n = normalise(u)
    for k, v in UNIT_ALIASES.items():
        if n == normalise(k):
            return v, mult
    return None, mult


def convert(
    value: float | None, from_unit: str | None, to_unit: str | None, substance: str | None = None
) -> float | None:
    """Convert `value` between units. Returns None when the conversion is impossible or ambiguous
    (unknown unit, mass <-> volume, IU for a substance without a known factor): callers then skip
    the comparison rather than guess."""
    if value is None:
        return None
    fu, fm = canonical_unit(from_unit)
    tu, tm = canonical_unit(to_unit)
    if fu is None or tu is None:
        return None
    v = value * fm / tm
    if fu == tu:
        return v
    if fu in MASS_UG and tu in MASS_UG:
        return v * MASS_UG[fu] / MASS_UG[tu]
    if fu == "ui" and tu in MASS_UG and substance:
        s = normalise(substance)
        for key, factor in UI_TO_UG.items():
            if key in s:
                return v * factor / MASS_UG[tu]
        return None
    vol = {"ml": 1.0, "cl": 10.0, "l": 1000.0}
    if fu in vol and tu in vol:
        return v * vol[fu] / vol[tu]
    return None
