"""Article calculation as a PURE FUNCTION: a faithful port of Declaration.assign_calculated_article
(data/models/declaration.py:569) that works on an in-memory composition instead of the ORM.

The same function is used to:
- check parity with the app (`cli parity`: recomputed article vs the article stored in the database,
  100 % on 300 recent declarations);
- compute the COUNTERFACTUAL ARTICLE: the article the declaration would have had if the
  composition actually read on the label had been declared ("undeclared active ingredient" fraud,
  rules.rule_counterfactual_article).

Recommendation: eventually replace the body of assign_calculated_article with a call to this
function (a single regulatory logic, no possible divergence).

The `reasons` strings are in French: they are quoted in findings shown to the declarant.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .refdata import AUTHORIZED, NOT_AUTHORIZED, REVOKED, RefData

ART_15 = "ART_15"
ART_15_WARNING = "ART_15_WARNING"
ART_15_HIGH_RISK_POPULATION = "ART_15_HIGH_RISK_POPULATION"
ART_16 = "ART_16"
ART_18 = "ART_18"
ANSES_REFERAL = "ANSES_REFERAL"
# Articles eligible for automatic validation (config/tasks.py): the scope of the fraud check.
AUTO_VALIDABLE = {ART_15, ART_15_WARNING, ART_15_HIGH_RISK_POPULATION}
# How constraining an article is: a counterfactual article of higher rank means the label escalates the procedure.
RANK = {
    "": 0,
    None: 0,
    ART_15: 1,
    ART_15_HIGH_RISK_POPULATION: 2,
    ART_15_WARNING: 2,
    ART_16: 3,
    ANSES_REFERAL: 4,
    ART_18: 4,
}
REPLACED = "REPLACED"
# Plants containing hydroxyanthracene derivatives are always "to be monitored" (same regex as the app).
HAD_REGEX = re.compile("dérivés hydroxyanthracéniques|dérivés anthracéniques|HAD", re.IGNORECASE)


@dataclass
class CompItem:
    kind: str
    uid: str | None
    new: bool = False
    request_status: str | None = None
    is_part_request: bool = False
    used_part_id: int | None = None
    preparation_id: int | None = None
    quantity: float | None = None
    unit_id: int | None = None
    source: str = "declared"  # declared | label (added from what the label shows)


@dataclass
class CompSubstance:
    uid: str
    quantity: float | None
    unit_id: int | None = None
    source: str = "declared"


@dataclass
class Composition:
    declaration_id: int | None
    items: list[CompItem] = field(default_factory=list)
    computed_substances: list[CompSubstance] = field(default_factory=list)
    populations: list[int] = field(default_factory=list)
    galenic_formulation_id: int | None = None
    siccrf_id: int | None = None


@dataclass
class ArticleResult:
    article: str | None
    reasons: list[str]


def _exceeded(ref: RefData, uid: str, quantity: float | None, populations: list[int]) -> bool:
    el = ref.get(uid)
    if el is None or quantity is None:
        return False
    mx = ref.max_for(el, populations)
    return mx is not None and quantity > mx


def compute_article(comp: Composition, ref: RefData) -> ArticleResult:
    """Regulatory article of a composition. The checks run in the same order as in the app,
    and the first one that matches wins."""
    # Historical declarations imported from Teleicare keep the article they were given.
    if comp.siccrf_id is not None:
        return ArticleResult(None, ["déclaration historique Teleicare : article déjà assigné"])
    if not comp.items and not comp.computed_substances:
        return ArticleResult("", ["composition vide"])

    # 1. A substance above its max dose: ART_18 for a nutrient (vitamin, mineral), else an ANSES referral.
    pops = comp.populations
    subs = [(s.uid, s.quantity, "calculée") for s in comp.computed_substances]
    subs += [(i.uid, i.quantity, "déclarée") for i in comp.items if i.kind == "substance" and i.uid]
    exceeded = [(uid, q, origin) for uid, q, origin in subs if _exceeded(ref, uid, q, pops)]
    if exceeded:
        nutrients = [e for e in exceeded if ref.get(e[0]).is_nutrient]
        names = ", ".join(
            f"{ref.get(u).name} {q:g} > max {ref.max_for(ref.get(u), pops):g}" for u, q, _ in (nutrients or exceeded)
        )
        if nutrients:
            return ArticleResult(ART_18, [f"nutriment au-delà de la dose max : {names}"])
        return ArticleResult(ANSES_REFERAL, [f"substance au-delà de la dose max : {names}"])

    def with_status(status):
        return [i for i in comp.items if i.uid and ref.get(i.uid) and ref.get(i.uid).status == status]

    # 2. A non-authorised or revoked element: ART_16.
    if unauth := with_status(NOT_AUTHORIZED):
        return ArticleResult(ART_16, ["élément non autorisé : " + ", ".join(ref.get(i.uid).name for i in unauth)])
    if revoked := with_status(REVOKED):
        return ArticleResult(ART_16, ["élément retiré : " + ", ".join(ref.get(i.uid).name for i in revoked)])

    # 3. A new element or plant part (pending request, or created by this very declaration): ART_16.
    ongoing_new = [i for i in comp.items if i.new and i.request_status != REPLACED]
    created = [
        i
        for i in comp.items
        if i.request_status == REPLACED
        and i.uid
        and ref.get(i.uid)
        and ref.get(i.uid).origin_declaration_id == comp.declaration_id
        and comp.declaration_id is not None
    ]
    part_requests = [i for i in comp.items if i.kind == "plant" and i.is_part_request]
    new_parts = [i for i in part_requests if i.request_status != REPLACED]
    created_parts = []
    for i in part_requests:
        if i.request_status == REPLACED and i.uid:
            part = ref.parts_by_plant.get(i.uid.split(":")[1], {}).get(str(i.used_part_id))
            if part and part.get("origin") == comp.declaration_id and comp.declaration_id is not None:
                created_parts.append(i)
    if ongoing_new or created or new_parts or created_parts:
        reasons = []
        if ongoing_new:
            reasons.append(
                "ingrédient nouveau (absent du référentiel) : "
                + ", ".join(
                    (ref.get(i.uid).name if i.uid and ref.get(i.uid) else "?") if i.uid else "nouvel ingrédient"
                    for i in ongoing_new
                )
            )
        if created:
            reasons.append("ingrédient créé suite à cette déclaration")
        if new_parts or created_parts:
            reasons.append("demande de partie de plante")
        return ArticleResult(ART_16, reasons)

    # 4. An element "to be monitored", a plant with hydroxyanthracene derivatives, an alcoholic
    #    preparation or a risky galenic form: ART_15_WARNING.
    risky = []
    for i in comp.items:
        el = ref.get(i.uid)
        if el is None or i.new:
            continue
        if el.is_risky:
            risky.append(el.name)
        elif i.kind == "plant" and HAD_REGEX.search(el.name):
            risky.append(el.name)
        if i.kind == "plant" and i.preparation_id is not None:
            prep = ref.preparations.get(str(i.preparation_id))
            if prep and prep["contains_alcohol"]:
                risky.append(f"{el.name} ({prep['name']}, contient de l'alcool)")
    for s in comp.computed_substances:
        el = ref.get(s.uid)
        if el and el.is_risky:
            risky.append(el.name)
    galenic = ref.galenic.get(str(comp.galenic_formulation_id)) if comp.galenic_formulation_id else None
    if risky or (galenic and galenic["is_risky"]):
        why = ["ingrédient à surveiller : " + ", ".join(sorted(set(risky)))] if risky else []
        if galenic and galenic["is_risky"]:
            why.append(f"forme galénique à risque : {galenic['name']}")
        return ArticleResult(ART_15_WARNING, why)
    # 5. A population defined as at risk by ANSES: ART_15_HIGH_RISK_POPULATION. Otherwise: ART_15.
    anses_pops = [
        ref.populations[str(p)]["name"] for p in pops if ref.populations.get(str(p), {}).get("is_defined_by_anses")
    ]
    if anses_pops:
        return ArticleResult(ART_15_HIGH_RISK_POPULATION, ["population à risque : " + ", ".join(anses_pops)])
    return ArticleResult(ART_15, [])


def composition_from_declaration(decl, ref: RefData) -> Composition:
    """The composition "as declared", built from a DeclarationDTO."""
    return Composition(
        declaration_id=decl.declaration_id,
        items=[
            CompItem(
                kind=i.kind,
                uid=i.uid,
                new=i.new,
                request_status=i.request_status,
                is_part_request=i.is_part_request,
                used_part_id=i.used_part_id,
                preparation_id=i.preparation_id,
                quantity=i.quantity,
                unit_id=i.unit_id,
            )
            for i in decl.items
        ],
        computed_substances=[
            CompSubstance(uid=c.uid, quantity=c.quantity, unit_id=c.unit_id) for c in decl.computed_substances
        ],
        populations=list(decl.populations),
        galenic_formulation_id=decl.galenic_formulation_id,
        siccrf_id=decl.siccrf_id,
    )


__all__ = ["AUTHORIZED", "AUTO_VALIDABLE", "RANK", "compute_article", "composition_from_declaration"]
