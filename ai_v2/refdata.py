"""Reference data (plants, substances, ingredients, micro-organisms, max doses, warnings...).

Loaded once from the database (read-only), then frozen in a local timestamped file: each run
records the exact version of the reference data it used (reproducibility). In production, the
same interface can be fed by the Django ORM instead of raw SQL.

Every element gets a uid "<kind>:<id>" (e.g. "plant:123"), because ids are only unique per table.
"""

from __future__ import annotations

import gzip
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .cache import stable_hash
from .config import Settings
from .db import fetchall
from .text import normalise

# Constants mirrored from the Django app (keep in sync):
# data/models/ingredient_status.py
AUTHORIZED, NOT_AUTHORIZED, NO_STATUS, REVOKED = 1, 2, 3, 99
# data/models/ingredient_type.py
FORM_OF_SUPPLY, ADDITIVE, AROMA, ACTIVE_INGREDIENT, NON_ACTIVE_INGREDIENT = 1, 2, 3, 4, 5
ACTIVE_INGREDIENT_TYPES = (FORM_OF_SUPPLY, ACTIVE_INGREDIENT)
# data/models/substance.py
VITAMIN, MINERAL = 1, 2

KINDS = ("plant", "substance", "ingredient", "microorganism")
# French labels of the kinds, used in text shown to the models and in finding details.
KIND_FR = {"plant": "plante", "substance": "substance", "ingredient": "ingrédient", "microorganism": "micro-organisme"}


@dataclass
class Element:
    """One element of the reference data, whatever its table."""

    uid: str
    kind: str
    id: int
    name: str
    synonyms: list[str] = field(default_factory=list)
    status: int | None = None
    is_risky: bool = False  # "to be monitored": makes the declaration ART_15_WARNING at least
    novel_food: bool = False
    is_obsolete: bool = False
    ingredient_type: int | None = None
    substance_types: list[int] = field(default_factory=list)
    cas: str | None = None
    unit_id: int | None = None
    warnings: list[str] = field(default_factory=list)  # mandatory label warnings (warnings_on_label)
    max_by_population: dict[str, float] = field(default_factory=dict)  # population_id (str) -> max
    must_specify_quantity: bool = False
    substances: list[str] = field(default_factory=list)  # uids of the substances it provides
    family: str | None = None
    origin_declaration_id: int | None = None  # declaration whose request created the element

    @property
    def active(self) -> bool:
        if self.kind == "ingredient":
            return self.ingredient_type in ACTIVE_INGREDIENT_TYPES
        return True

    @property
    def is_nutrient(self) -> bool:
        return self.kind == "substance" and bool({VITAMIN, MINERAL} & set(self.substance_types))

    def label(self) -> str:
        return f"{self.name} [{KIND_FR[self.kind]}]"


@dataclass
class RefData:
    version: str  # hash of the elements and plant parts: identifies the snapshot in run manifests
    loaded_at: float
    elements: dict[str, Element]
    plant_parts: dict[str, str]  # plantpart_id -> name
    parts_by_plant: dict[str, dict[str, dict]]  # plant_id -> {plantpart_id: {status, origin}}
    preparations: dict[str, dict]  # id -> {name, contains_alcohol}
    units: dict[str, dict]  # id -> {name, long_name}
    populations: dict[str, dict]  # id -> {name, is_defined_by_anses, min_age, max_age}
    galenic: dict[str, dict]  # id -> {name, is_risky, is_liquid}
    conditions: dict[str, str]  # id -> name
    general_population_id: str | None = None
    # derived (not serialised)
    sources_of_substance: dict[str, list[str]] = field(default_factory=dict)

    def __post_init__(self):
        if not self.sources_of_substance:
            for el in self.elements.values():
                for s in el.substances:
                    self.sources_of_substance.setdefault(s, []).append(el.uid)

    def get(self, uid: str | None) -> Element | None:
        return self.elements.get(uid) if uid else None

    def unit_name(self, unit_id) -> str | None:
        u = self.units.get(str(unit_id)) if unit_id is not None else None
        return u["name"] if u else None

    def max_for(self, el: Element, population_ids: list[int] | None = None) -> float | None:
        """Max dose for the targeted populations. Same logic as Declaration._has_max_quantity_exceeded:
        the minimum over the targeted populations that have a max, plus the general population's max
        if some targeted populations have none; the general population's max when nothing is targeted."""
        pops = [str(p) for p in (population_ids or [])]
        targeted = [el.max_by_population[p] for p in pops if p in el.max_by_population]
        general = el.max_by_population.get(self.general_population_id or "")
        if targeted:
            return min(targeted + ([general] if general is not None and len(targeted) < len(pops) else []))
        return general

    def searchable_strings(self) -> list[tuple[str, str]]:
        """(text, uid) pairs for the search index: names + synonyms of the non-obsolete elements."""
        out = []
        for el in self.elements.values():
            if el.is_obsolete:
                continue
            out.append((el.name, el.uid))
            out.extend((s, el.uid) for s in el.synonyms if s)
        return out

    # ------------------------------------------------------------------ persistence
    def to_json(self) -> dict:
        d = asdict(self)
        d.pop("sources_of_substance", None)
        return d

    @classmethod
    def from_json(cls, d: dict) -> "RefData":
        d = dict(d)
        d["elements"] = {k: Element(**v) for k, v in d["elements"].items()}
        return cls(**d)


def _load_from_db(settings: Settings) -> RefData:
    """Read the whole reference data from the app's tables (about 20 SELECTs)."""
    q = lambda sql: fetchall(settings, sql)  # noqa: E731
    elements: dict[str, Element] = {}

    for r in q(
        """select p.id, p.name, p.status, p.is_risky, p.novel_food, p.is_obsolete, p.unit_id,
                  p.warnings_on_label, f.name family, p.origin_declaration_id from data_plant p left join data_plantfamily f on f.id=p.family_id"""
    ):
        elements[f"plant:{r['id']}"] = Element(
            uid=f"plant:{r['id']}",
            kind="plant",
            id=r["id"],
            name=r["name"],
            status=r["status"],
            is_risky=r["is_risky"],
            novel_food=r["novel_food"],
            is_obsolete=r["is_obsolete"],
            unit_id=r["unit_id"],
            warnings=list(r["warnings_on_label"] or []),
            family=r["family"],
            origin_declaration_id=r["origin_declaration_id"],
        )
    for r in q(
        """select id, name, status, is_risky, novel_food, is_obsolete, unit_id, warnings_on_label, substance_types,
                  cas_number, must_specify_quantity, origin_declaration_id from data_substance"""
    ):
        elements[f"substance:{r['id']}"] = Element(
            uid=f"substance:{r['id']}",
            kind="substance",
            id=r["id"],
            name=r["name"],
            status=r["status"],
            is_risky=r["is_risky"],
            novel_food=r["novel_food"],
            is_obsolete=r["is_obsolete"],
            unit_id=r["unit_id"],
            warnings=list(r["warnings_on_label"] or []),
            substance_types=list(r["substance_types"] or []),
            cas=r["cas_number"],
            must_specify_quantity=r["must_specify_quantity"],
            origin_declaration_id=r["origin_declaration_id"],
        )
    for r in q(
        """select id, name, status, is_risky, novel_food, is_obsolete, unit_id, warnings_on_label, ingredient_type, origin_declaration_id
           from data_ingredient"""
    ):
        elements[f"ingredient:{r['id']}"] = Element(
            uid=f"ingredient:{r['id']}",
            kind="ingredient",
            id=r["id"],
            name=r["name"],
            status=r["status"],
            is_risky=r["is_risky"],
            novel_food=r["novel_food"],
            is_obsolete=r["is_obsolete"],
            unit_id=r["unit_id"],
            warnings=list(r["warnings_on_label"] or []),
            ingredient_type=r["ingredient_type"],
            origin_declaration_id=r["origin_declaration_id"],
        )
    for r in q(
        """select id, coalesce(nullif(name,''), trim(coalesce(genus,'')||' '||coalesce(species,''))) name, status,
                  is_risky, novel_food, is_obsolete, unit_id, warnings_on_label, origin_declaration_id from data_microorganism"""
    ):
        elements[f"microorganism:{r['id']}"] = Element(
            uid=f"microorganism:{r['id']}",
            kind="microorganism",
            id=r["id"],
            name=r["name"],
            status=r["status"],
            is_risky=r["is_risky"],
            novel_food=r["novel_food"],
            is_obsolete=r["is_obsolete"],
            unit_id=r["unit_id"],
            warnings=list(r["warnings_on_label"] or []),
            origin_declaration_id=r["origin_declaration_id"],
        )

    # Synonyms and per-population max doses share the same table layout for the four kinds.
    for kind in KINDS:
        for r in q(f"select standard_name_id sid, name from data_{kind}synonym"):
            el = elements.get(f"{kind}:{r['sid']}")
            if el and r["name"] and normalise(r["name"]) != normalise(el.name):
                el.synonyms.append(r["name"])
        for r in q(
            f"select {kind}_id eid, population_id pid, max_quantity mq from data_{kind}maxquantityperpopulationrelation"
        ):
            el = elements.get(f"{kind}:{r['eid']}")
            if el and r["mq"] is not None:
                el.max_by_population[str(r["pid"])] = r["mq"]

    # Hierarchy: which substances a plant or an ingredient (form of supply) provides.
    for r in q("select plant_id a, substance_id b from data_plantsubstancerelation"):
        el = elements.get(f"plant:{r['a']}")
        if el:
            el.substances.append(f"substance:{r['b']}")
    for r in q("select ingredient_id a, substance_id b from data_ingredientsubstancerelation"):
        el = elements.get(f"ingredient:{r['a']}")
        if el:
            el.substances.append(f"substance:{r['b']}")

    plant_parts = {str(r["id"]): r["name"] for r in q("select id, name from data_plantpart")}
    parts_by_plant: dict[str, dict[str, dict]] = {}
    for r in q("select plant_id, plantpart_id, status, origin_declaration_id from data_part"):
        parts_by_plant.setdefault(str(r["plant_id"]), {})[str(r["plantpart_id"])] = {
            "status": r["status"],
            "origin": r["origin_declaration_id"],
        }
    preparations = {
        str(r["id"]): {"name": r["name"], "contains_alcohol": r["contains_alcohol"]}
        for r in q("select id, name, contains_alcohol from data_preparation")
    }
    units = {
        str(r["id"]): {"name": r["name"], "long_name": r["long_name"]}
        for r in q("select id, name, long_name from data_unit")
    }
    populations = {
        str(r["id"]): {
            "name": r["name"],
            "is_defined_by_anses": r["is_defined_by_anses"],
            "min_age": r["min_age"],
            "max_age": r["max_age"],
            "is_obsolete": r["is_obsolete"],
        }
        for r in q("select id, name, is_defined_by_anses, min_age, max_age, is_obsolete from data_population")
    }
    galenic = {
        str(r["id"]): {"name": r["name"], "is_risky": r["is_risky"], "is_liquid": r["is_liquid"]}
        for r in q("select id, name, is_risky, is_liquid from data_galenicformulation")
    }
    conditions = {str(r["id"]): r["name"] for r in q("select id, name from data_condition")}
    # "Population générale" is the name stored in the database.
    general = next((pid for pid, p in populations.items() if p["name"] == "Population générale"), None)

    body = {"elements": {k: asdict(v) for k, v in elements.items()}, "parts": parts_by_plant}
    return RefData(
        version=stable_hash(body)[:12],
        loaded_at=time.time(),
        elements=elements,
        plant_parts=plant_parts,
        parts_by_plant=parts_by_plant,
        preparations=preparations,
        units=units,
        populations=populations,
        galenic=galenic,
        conditions=conditions,
        general_population_id=general,
    )


def load_refdata(settings: Settings, refresh: bool = False, max_age_h: float = 24.0) -> RefData:
    """Latest frozen snapshot if it is less than `max_age_h` old, else a fresh load from the database."""
    folder = settings.data_dir / "refdata"
    folder.mkdir(parents=True, exist_ok=True)
    existing = sorted(folder.glob("refdata_*.json.gz"))
    if existing and not refresh:
        latest = existing[-1]
        if time.time() - latest.stat().st_mtime < max_age_h * 3600:
            with gzip.open(latest, "rt", encoding="utf-8") as f:
                return RefData.from_json(json.load(f))
    ref = _load_from_db(settings)
    path: Path = folder / f"refdata_{time.strftime('%Y%m%d-%H%M%S')}_{ref.version}.json.gz"
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(ref.to_json(), f, ensure_ascii=False)
    return ref
