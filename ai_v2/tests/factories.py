"""Synthetic data factories for the tests (no network, no database).

The reference data below is a tiny, made-up subset; element names are in French like the real data."""

from __future__ import annotations

import time

from ai_v2.declarations import ComputedSubstanceDTO, DeclarationDTO, DeclaredItem
from ai_v2.extract import FileExtraction, MergedLabel
from ai_v2.refdata import Element, RefData
from ai_v2.schemas import (
    Basis,
    CompositionRow,
    DailyDose,
    DocumentKind,
    LabelExtraction,
    LabelIngredient,
    Legibility,
    Mention,
    Mentions,
    MentionStatus,
    ProductIdentity,
    Resolution,
)

# population ids: general population, pregnant women
GEN, ENCEINTES = "1", "2"


def refdata() -> RefData:
    """Small reference data: authorised, non-authorised and risky plants, nutrients with max doses, additives."""
    els = [
        Element(uid="plant:1", kind="plant", id=1, name="Curcuma longa L.", synonyms=["curcuma"], status=1),
        Element(uid="plant:2", kind="plant", id=2, name="Ephedra sinica Stapf", status=2),  # not authorised
        Element(
            uid="plant:3",
            kind="plant",
            id=3,
            name="Camellia sinensis (L.) Kuntze",
            synonyms=["thé vert"],
            status=1,
            is_risky=True,
            warnings=["Déconseillé aux femmes enceintes."],
            substances=["substance:12"],
        ),
        Element(uid="plant:4", kind="plant", id=4, name="Rheum palmatum L. (dérivés hydroxyanthracéniques)", status=1),
        Element(
            uid="substance:10",
            kind="substance",
            id=10,
            name="zinc",
            status=1,
            substance_types=[2],
            unit_id=3,
            max_by_population={GEN: 15.0},
        ),
        Element(
            uid="substance:11",
            kind="substance",
            id=11,
            name="mélatonine",
            status=1,
            substance_types=[4],
            unit_id=3,
            max_by_population={GEN: 1.9},
        ),
        Element(
            uid="substance:12",
            kind="substance",
            id=12,
            name="caféine",
            status=1,
            substance_types=[3],
            unit_id=3,
            max_by_population={GEN: 200.0, ENCEINTES: 0.0},
        ),
        Element(
            uid="ingredient:20",
            kind="ingredient",
            id=20,
            name="hydroxypropylméthylcellulose",
            status=1,
            ingredient_type=2,
            synonyms=["E464", "HPMC"],
        ),
        Element(
            uid="ingredient:21",
            kind="ingredient",
            id=21,
            name="gluconate de zinc",
            status=1,
            ingredient_type=1,
            substances=["substance:10"],
        ),
    ]
    return RefData(
        version="test",
        loaded_at=time.time(),
        elements={e.uid: e for e in els},
        plant_parts={"1": "Racine", "2": "Feuille"},
        parts_by_plant={"1": {"1": {"status": 1, "origin": None}}},
        preparations={"5": {"name": "Teinture", "contains_alcohol": True}},
        units={
            "1": {"name": "µg", "long_name": ""},
            "2": {"name": "g", "long_name": ""},
            "3": {"name": "mg", "long_name": ""},
        },
        populations={
            GEN: {
                "name": "Population générale",
                "is_defined_by_anses": False,
                "min_age": None,
                "max_age": None,
                "is_obsolete": False,
            },
            ENCEINTES: {
                "name": "Femmes enceintes",
                "is_defined_by_anses": True,
                "min_age": None,
                "max_age": None,
                "is_obsolete": False,
            },
        },
        galenic={
            "1": {"name": "Gélule", "is_risky": False, "is_liquid": False},
            "9": {"name": "Spray", "is_risky": True, "is_liquid": True},
        },
        conditions={},
        general_population_id=GEN,
    )


def declaration(
    items=None, computed=None, article="ART_15", populations=None, name="Produit Test", dose="2 gélules par jour"
):
    return DeclarationDTO(
        key="decl:1",
        declaration_id=1,
        name=name,
        brand="Marque",
        article=article,
        daily_recommended_dose=dose,
        galenic_formulation_id=1,
        populations=populations or [],
        items=items or [],
        computed_substances=computed or [],
    )


def item(kind, uid, name, quantity=None, unit_id=3, **kw):
    return DeclaredItem(kind=kind, uid=uid, name=name, quantity=quantity, unit_id=unit_id, **kw)


def computed(uid, name, q, unit_id=3):
    return ComputedSubstanceDTO(uid=uid, name=name, quantity=q, unit_id=unit_id)


def mention(status="present", quote="ok"):
    return Mention(status=MentionStatus(status), quote=quote if status == "present" else None, page=0)


def mentions(**overrides) -> Mentions:
    keys = Mentions.model_fields.keys()
    return Mentions(**{k: overrides.get(k, mention()) for k in keys})


def ingredient(raw, name=None, active=True, **kw):
    base = dict(
        raw=raw,
        name=name or raw,
        botanical_name=None,
        plant_part=None,
        preparation=None,
        extract_ratio=None,
        standardisation=[],
        e_number=None,
        functional_class=None,
        is_capsule_shell=False,
        is_active=active,
        quantity=None,
        unit=None,
        basis=Basis.unknown,
        percentage=None,
        from_premix=None,
        page=0,
    )
    base.update(kw)
    return LabelIngredient(**base)


def comp_row(raw, name, value, unit, basis=Basis.per_daily_dose, basis_text=None):
    return CompositionRow(
        raw=raw,
        name=name,
        value=value,
        unit=unit,
        basis=basis,
        basis_text=basis_text,
        nrv_percent=None,
        is_sub_row=False,
        parent=None,
        page=0,
    )


def label(
    ingredients=(),
    composition=(),
    ments=None,
    text="",
    units_per_day=2,
    kind=DocumentKind.packaging_artwork,
    legibility=Legibility.good,
    french=True,
    anomalies=(),
) -> MergedLabel:
    """A one-file label. `text` is its OCR text (by default, the ingredient and composition wordings)."""
    ex = LabelExtraction(
        is_food_supplement_label=kind in (DocumentKind.packaging_artwork, DocumentKind.label_photo),
        document_kind=kind,
        legibility=legibility,
        languages=["fr"],
        french_present=french,
        product=ProductIdentity(
            name="Produit Test", brand="Marque", galenic_form="gélule", net_quantity="60 gélules", unit_count=60
        ),
        daily_dose=DailyDose(text="2 gélules par jour", units_per_day_max=units_per_day, unit_kind="gélule", page=0),
        ingredients=list(ingredients),
        composition=list(composition),
        mentions=ments or mentions(),
        warnings=[],
        claims=[],
        target_populations=[],
        anomalies=list(anomalies),
    )
    full = text or " ".join([i.raw for i in ingredients] + [c.raw for c in composition]) + " Produit Test Marque"
    fe = FileExtraction(url="u", sha256="s", kind="pdf", n_pages_total=1, ocr_pages=[full], extraction=ex)
    from ai_v2.extract import grounding_report

    fe.grounding = grounding_report(fe)
    return MergedLabel(files=[fe])


def resolution(text, uid, conf=0.95, method="exact"):
    return Resolution(text=text, uid=uid, confidence=conf, method=method)
