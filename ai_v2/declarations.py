"""Loading a declaration in a neutral form (DTO), either in its current state (tables) or in the
exact state an instructor saw at a given time (snapshot.json_declaration).

The second mode is essential for evaluation: when an instructor blocked a declaration because it
did not match its label, the declarant has often fixed it since. We must therefore replay the
composition AND the label as they were when the instructor blocked it.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .config import Settings
from .db import fetchall, fetchone


class DeclaredItem(BaseModel):
    """One declared plant, ingredient, substance or micro-organism."""

    kind: str  # plant | substance | ingredient | microorganism
    uid: str | None = None  # None for a new element (not in the reference data yet)
    name: str = ""
    active: bool = True
    new: bool = False
    quantity: float | None = None
    unit_id: int | None = None
    used_part_id: int | None = None
    preparation_id: int | None = None
    request_status: str | None = None
    is_part_request: bool = False


class ComputedSubstanceDTO(BaseModel):
    """Substance quantity computed by the app from the declared items (data_computedsubstance)."""

    uid: str
    name: str = ""
    quantity: float | None = None
    unit_id: int | None = None


class AttachmentDTO(BaseModel):
    id: int | None = None
    type: str | None = None  # "LABEL" for label files
    url: str
    name: str = ""


class DeclarationDTO(BaseModel):
    key: str  # "decl:<id>" (current state) or "snap:<snapshot id>" (state at a snapshot)
    declaration_id: int
    snapshot_id: int | None = None
    source: str = "current"
    status: str | None = None
    article: str | None = None
    calculated_article: str | None = None
    siccrf_id: int | None = None  # set for historical (Teleicare) declarations
    company_id: int | None = None
    name: str = ""
    brand: str = ""
    gamme: str = ""
    galenic_formulation_id: int | None = None
    other_galenic_formulation: str = ""
    unit_quantity: float | None = None
    unit_measurement_id: int | None = None
    conditioning: str = ""
    daily_recommended_dose: str = ""
    instructions: str = ""
    warning: str = ""
    populations: list[int] = Field(default_factory=list)
    conditions: list[int] = Field(default_factory=list)
    items: list[DeclaredItem] = Field(default_factory=list)
    computed_substances: list[ComputedSubstanceDTO] = Field(default_factory=list)
    attachments: list[AttachmentDTO] = Field(default_factory=list)

    @property
    def labels(self) -> list[AttachmentDTO]:
        return [a for a in self.attachments if a.type == "LABEL"]

    def summary_for_llm(self) -> str:
        """Plain-text summary of the declaration for the verification agent (model input, in French)."""
        lines = [
            f"Produit : {self.name} (marque : {self.brand or '-'})",
            f"DJR déclarée : {self.daily_recommended_dose}",
        ]
        for it in self.items:
            q = f" — {it.quantity:g} (unit_id {it.unit_id})" if it.quantity is not None else ""
            lines.append(
                f"- [{it.kind}{', nouveau' if it.new else ''}{', inactif' if not it.active else ''}] {it.name}{q}"
            )
        for cs in self.computed_substances:
            q = f" — {cs.quantity:g} (unit_id {cs.unit_id})" if cs.quantity is not None else ""
            lines.append(f"- [substance calculée] {cs.name}{q}")
        return "\n".join(lines)


def _media_url(settings: Settings, path: str) -> str:
    """Absolute URL of an attachment (the database stores paths relative to the media bucket)."""
    if path.startswith("http"):
        return path
    if not settings.media_base_url:
        raise RuntimeError("AI_V2_MEDIA_BASE_URL is not set (base URL of the media bucket, ending with '/').")
    return settings.media_base_url + path.lstrip("/")


# ---------------------------------------------------------------------------------------- current state
def load_current(settings: Settings, declaration_id: int) -> DeclarationDTO:
    """The declaration as it is now in the tables."""
    d = fetchone(settings, "select * from data_declaration where id=%s", (declaration_id,))
    if d is None:
        raise KeyError(declaration_id)
    items: list[DeclaredItem] = []
    for r in fetchall(
        settings,
        """select x.*, p.name el_name from data_declaredplant x left join data_plant p on p.id=x.plant_id
           where x.declaration_id=%s order by x.id""",
        (declaration_id,),
    ):
        items.append(
            DeclaredItem(
                kind="plant",
                uid=f"plant:{r['plant_id']}" if r["plant_id"] else None,
                name=r["el_name"] or r["new_name"],
                active=r["active"],
                new=r["new"],
                quantity=r["quantity"],
                unit_id=r["unit_id"],
                used_part_id=r["used_part_id"],
                preparation_id=r["preparation_id"],
                request_status=r["request_status"],
                is_part_request=r["is_part_request"],
            )
        )
    for kind, fk in (("ingredient", "ingredient_id"), ("substance", "substance_id")):
        for r in fetchall(
            settings,
            f"""select x.*, e.name el_name from data_declared{kind} x left join data_{kind} e on e.id=x.{fk}
                where x.declaration_id=%s order by x.id""",
            (declaration_id,),
        ):
            items.append(
                DeclaredItem(
                    kind=kind,
                    uid=f"{kind}:{r[fk]}" if r[fk] else None,
                    name=r["el_name"] or r["new_name"],
                    active=r["active"],
                    new=r["new"],
                    quantity=r["quantity"],
                    unit_id=r["unit_id"],
                    request_status=r["request_status"],
                )
            )
    for r in fetchall(
        settings,
        """select x.*, coalesce(nullif(e.name,''), e.genus||' '||e.species) el_name from data_declaredmicroorganism x
           left join data_microorganism e on e.id=x.microorganism_id where x.declaration_id=%s order by x.id""",
        (declaration_id,),
    ):
        items.append(
            DeclaredItem(
                kind="microorganism",
                uid=f"microorganism:{r['microorganism_id']}" if r["microorganism_id"] else None,
                name=r["el_name"] or f"{r['new_genre']} {r['new_species']}".strip(),
                active=r["active"],
                new=r["new"],
                quantity=r["quantity"],
                request_status=r["request_status"],
            )
        )
    computed = [
        ComputedSubstanceDTO(
            uid=f"substance:{r['substance_id']}", name=r["name"], quantity=r["quantity"], unit_id=r["unit_id"]
        )
        for r in fetchall(
            settings,
            """select c.substance_id, c.quantity, c.unit_id, s.name from data_computedsubstance c
               join data_substance s on s.id=c.substance_id where c.declaration_id=%s""",
            (declaration_id,),
        )
    ]
    attachments = [
        AttachmentDTO(id=r["id"], type=r["type"], url=_media_url(settings, r["file"]), name=r["name"] or "")
        for r in fetchall(
            settings,
            "select id, type, file, name from data_attachment where declaration_id=%s order by id",
            (declaration_id,),
        )
    ]
    pops = [
        r["population_id"]
        for r in fetchall(
            settings,
            "select population_id from data_declaration_populations where declaration_id=%s",
            (declaration_id,),
        )
    ]
    conds = [
        r["condition_id"]
        for r in fetchall(
            settings,
            "select condition_id from data_declaration_conditions_not_recommended where declaration_id=%s",
            (declaration_id,),
        )
    ]
    return DeclarationDTO(
        key=f"decl:{declaration_id}",
        declaration_id=declaration_id,
        source="current",
        status=d["status"],
        article=d["article"],
        calculated_article=d["calculated_article"],
        siccrf_id=d["siccrf_id"],
        company_id=d["company_id"],
        name=d["name"] or "",
        brand=d["brand"] or "",
        gamme=d["gamme"] or "",
        galenic_formulation_id=d["galenic_formulation_id"],
        other_galenic_formulation=d["other_galenic_formulation"] or "",
        unit_quantity=d["unit_quantity"],
        unit_measurement_id=d["unit_measurement_id"],
        conditioning=d["conditioning"] or "",
        daily_recommended_dose=d["daily_recommended_dose"] or "",
        instructions=d["instructions"] or "",
        warning=d["warning"] or "",
        populations=pops,
        conditions=conds,
        items=items,
        computed_substances=computed,
        attachments=attachments,
    )


# ---------------------------------------------------------------------------------------- snapshot
def _id(v):
    """Snapshot JSON stores foreign keys either as an id or as a nested object with an "id"."""
    if isinstance(v, dict):
        return v.get("id")
    return v


def from_snapshot_json(settings: Settings, snapshot_id: int, declaration_id: int, j: dict) -> DeclarationDTO:
    """Build the DTO from a snapshot's json_declaration (the API serialisation, in camelCase)."""
    items: list[DeclaredItem] = []
    for key, kind in (
        ("declaredPlants", "plant"),
        ("declaredIngredients", "ingredient"),
        ("declaredSubstances", "substance"),
        ("declaredMicroorganisms", "microorganism"),
    ):
        for x in j.get(key) or []:
            el = x.get("element") or {}
            name = el.get("name") or x.get("newName") or ""
            if kind == "microorganism" and not name:
                name = f"{x.get('newGenre', '')} {x.get('newSpecies', '')}".strip()
            items.append(
                DeclaredItem(
                    kind=kind,
                    uid=f"{kind}:{el['id']}" if el.get("id") else None,
                    name=name,
                    active=bool(x.get("active", True)),
                    new=bool(x.get("new", False)),
                    quantity=x.get("quantity"),
                    unit_id=_id(x.get("unit")),
                    used_part_id=_id(x.get("usedPart")),
                    preparation_id=_id(x.get("preparation")),
                    request_status=x.get("requestStatus"),
                    is_part_request=bool(x.get("isPartRequest", False)),
                )
            )
    computed = []
    for x in j.get("computedSubstances") or []:
        s = x.get("substance") or {}
        if s.get("id"):
            computed.append(
                ComputedSubstanceDTO(
                    uid=f"substance:{s['id']}",
                    name=s.get("name", ""),
                    quantity=x.get("quantity"),
                    unit_id=_id(x.get("unit")),
                )
            )
    attachments = [
        AttachmentDTO(
            id=a.get("id"), type=a.get("type"), url=_media_url(settings, a.get("file", "")), name=a.get("name") or ""
        )
        for a in j.get("attachments") or []
        if a.get("file")
    ]
    company = j.get("company")
    return DeclarationDTO(
        key=f"snap:{snapshot_id}",
        declaration_id=declaration_id,
        snapshot_id=snapshot_id,
        source="snapshot",
        status=j.get("status"),
        article=j.get("article"),
        calculated_article=j.get("calculatedArticle"),
        siccrf_id=j.get("siccrfId"),
        company_id=_id(company),
        name=j.get("name") or "",
        brand=j.get("brand") or "",
        gamme=j.get("gamme") or "",
        galenic_formulation_id=_id(j.get("galenicFormulation")),
        other_galenic_formulation=j.get("otherGalenicFormulation") or "",
        unit_quantity=j.get("unitQuantity"),
        unit_measurement_id=_id(j.get("unitMeasurement")),
        conditioning=j.get("conditioning") or "",
        daily_recommended_dose=j.get("dailyRecommendedDose") or "",
        instructions=j.get("instructions") or "",
        warning=j.get("warning") or "",
        populations=[_id(p) for p in j.get("populations") or []],
        conditions=[_id(c) for c in j.get("conditionsNotRecommended") or []],
        items=items,
        computed_substances=computed,
        attachments=attachments,
    )


def load_snapshot(settings: Settings, snapshot_id: int) -> DeclarationDTO:
    """The declaration as it was at `snapshot_id` (composition and label files of that time)."""
    r = fetchone(
        settings, "select id, declaration_id, json_declaration from data_snapshot where id=%s", (snapshot_id,)
    )
    if r is None:
        raise KeyError(snapshot_id)
    j = r["json_declaration"]
    if isinstance(j, str):
        import json

        j = json.loads(j)
    return from_snapshot_json(settings, r["id"], r["declaration_id"], j)
