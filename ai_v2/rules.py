"""Stage 4: DETERMINISTIC rules engine (the code judges, not the LLM).

Each rule produces findings (Finding) with a severity, a fraud type, a confidence and evidence.
The only model calls here are short, cached semantic checks (is a reworded warning present?).

  R-ART   counterfactual article (composition read on the label -> recomputed article)
  R-DOSE  label quantities vs declaration vs max doses per population
  R-ING   completeness: label ingredients missing from the declaration
  R-MEN   mandatory statements (decree 2006-352 art. 10/12, INCO), with a text double-check
  R-WARN  mandatory warnings attached to ingredients (warnings_on_label), alcohol warning
  R-ID    identity: is this label the label of the declared product?
  R-DOC   fake document / illegible label / no French / placeholder text
  R-DJR   daily dose on the label vs declared, drops without a volume
  R-CLM   therapeutic claims

Conventions:
- Finding titles and details are in French: they are sent to the declarant (decision.build_message)
  and read by the verification agent.
- Regexes match the normalised text (text.normalise: lower case, no accents, no punctuation), so
  they are written without accents. They match French label wording on purpose.
- Confidence = how sure we are that the finding is true. It is lowered whenever the evidence is
  not grounded (quote not found in the label text, factor 0.6) or the label is hard to read.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from rapidfuzz import fuzz

from .article import (
    ART_15,
    ART_15_WARNING,
    AUTO_VALIDABLE,
    RANK,
    CompItem,
    CompSubstance,
    Composition,
    composition_from_declaration,
    compute_article,
)
from .config import Settings, prompt_hash, prompt_text
from .declarations import DeclarationDTO
from .extract import MergedLabel, grounded
from .llm import LLMClient
from .refdata import RefData
from .schemas import (
    Basis,
    Evidence,
    Finding,
    FraudType,
    LabelIngredient,
    MentionStatus,
    Resolution,
    Severity,
    WarningCheck,
)
from .text import contains_any, normalise, quote_in_text
from .units import convert

# Below this resolution confidence, a label row is not used to compute doses or the counterfactual article.
RESOLUTION_MIN_CONF = 0.75
# Relative difference tolerated between a label quantity and the declared quantity.
DOSE_TOLERANCE = 0.10
# "Équivalent plante : 2 g", "soit 1000 mg de plante sèche": an equivalence, not an ingredient quantity
EQUIVALENCE = re.compile(r"\b(equivalent|equiv|eq|correspond(ant)?|soit|ratio|der)\b")
# Wordings that are not ingredients but headers or cross-references ("voir tableau", "Mélange de...")
GENERIC = re.compile(
    r"(voir tableau|cf tableau|extraits? (secs? )?de plantes$|^melange|^complexe|^premix|^premelange|"
    r"^formule|^actifs?$|^plantes?$|^vitamines?$|^mineraux$|^ingredients?$|^excipients?$)"
)


def is_generic(row) -> bool:
    return bool(GENERIC.search(normalise(row.name))) or bool(GENERIC.search(normalise(row.raw)))


def row_is_active(ref, row) -> bool:
    """Active if the reference data AND the label reading agree (rice flour labelled as a "bulking
    agent" stays an excipient even though plants are "active" in the reference data)."""
    el = ref.get(row.resolution.uid)
    label_active = bool(row.ingredient.is_active) if row.ingredient else True
    if row.ingredient and row.ingredient.functional_class:
        label_active = False
    return (el.active and label_active) if el else label_active


@dataclass
class LabelRow:
    """One resolved row of the label: an ingredient-list entry or a composition-table row."""

    file_index: int
    kind: str  # ingredient | composition
    raw: str
    name: str
    page: int
    grounded: bool
    resolution: Resolution
    ingredient: LabelIngredient | None = None
    row: object | None = None  # the CompositionRow, for kind == "composition"
    matched_declared: int | None = None  # index in decl.items
    match_via: str | None = None  # how it was matched (uid, substance_of_declared, name...)


@dataclass
class Context:
    """Everything the rules need, plus what they produce (findings, and facts for the trace)."""

    settings: Settings
    ref: RefData
    decl: DeclarationDTO
    label: MergedLabel
    rows: list[LabelRow]
    findings: list[Finding] = field(default_factory=list)
    facts: dict = field(default_factory=dict)  # keys starting with "_" are internal, not saved

    def add(
        self,
        code: str,
        severity: Severity,
        fraud: FraudType,
        confidence: float,
        title: str,
        detail: str,
        evidence: list[Evidence] | None = None,
        grounded_: bool | None = None,
        refs: list[str] | None = None,
    ) -> Finding:
        # A finding without a quote (an ABSENCE: missing statement, no French...) is not "proven" by
        # itself: it can only block once confirmed by the agent.
        if grounded_ is None:
            grounded_ = bool(evidence)
        f = Finding(
            id=f"F{len(self.findings) + 1}",
            code=code,
            severity=severity,
            fraud_type=fraud,
            confidence=round(max(0.0, min(confidence, 1.0)), 3),
            title=title,
            detail=detail,
            evidence=evidence or [],
            grounded=grounded_,
            refs=refs or [],
        )
        self.findings.append(f)
        return f

    @property
    def ingredient_rows(self) -> list[LabelRow]:
        return [r for r in self.rows if r.kind == "ingredient"]

    @property
    def composition_rows(self) -> list[LabelRow]:
        return [r for r in self.rows if r.kind == "composition"]


# =============================================================================== matching
def match_rows_to_declaration(ctx: Context) -> None:
    """Match each label row to a declared element BY IDENTIFIER, using the reference data hierarchy
    (substance <-> form of supply / source plant), then by name for new elements.

    Sets row.matched_declared and row.match_via; every completeness rule depends on it.
    """
    ref, decl = ctx.ref, ctx.decl
    by_uid: dict[str, int] = {it.uid: i for i, it in enumerate(decl.items) if it.uid}
    computed_uids = {c.uid for c in decl.computed_substances}
    provides: dict[str, int] = {}  # substance uid -> index of the declared element that provides it
    for i, it in enumerate(decl.items):
        el = ref.get(it.uid)
        if el:
            for s in el.substances:
                provides.setdefault(s, i)
    for row in ctx.rows:
        uid = row.resolution.uid if row.resolution.confidence >= 0.5 else None
        # 1. Same element.
        if uid and uid in by_uid:
            row.matched_declared, row.match_via = by_uid[uid], "uid"
            continue
        el = ref.get(uid)
        # 2. A substance provided by a declared element ("zinc" on the label, "zinc gluconate" declared).
        if el and el.kind == "substance" and (uid in provides or uid in computed_uids):
            row.matched_declared, row.match_via = provides.get(uid), "substance_of_declared"
            continue
        # 3. A form of supply of a declared substance.
        if el and any(s in by_uid or s in computed_uids for s in el.substances):
            idx = next((by_uid[s] for s in el.substances if s in by_uid), None)
            row.matched_declared, row.match_via = idx, "form_of_declared_substance"
            continue
        # 4. Same species declared under another uid (synonymy in the reference data)?
        if el and el.kind == "plant":
            for i, it in enumerate(decl.items):
                if it.kind == "plant" and normalise(it.name).split()[:2] == normalise(el.name).split()[:2]:
                    row.matched_declared, row.match_via = i, "same_binomial"
                    break
            if row.matched_declared is not None:
                continue
        # 5. New elements declared by their name only, or a missed resolution: fuzzy name match.
        best, best_i = 0.0, None
        for i, it in enumerate(decl.items):
            score = max(
                fuzz.token_set_ratio(normalise(row.name), normalise(it.name)),
                fuzz.token_set_ratio(normalise(row.raw), normalise(it.name)),
            )
            if score > best:
                best, best_i = score, i
        if best >= 90:
            row.matched_declared, row.match_via = best_i, "name"


# =============================================================================== R-ING
def rule_completeness(ctx: Context) -> None:
    """Label ingredients that are not declared: one finding per ingredient, plus a global one
    when a large share of the label is undeclared (a sign of another product's label)."""
    ref = ctx.ref
    ing = ctx.ingredient_rows
    if not ing:
        return
    ing = [r for r in ing if not is_generic(r)]
    unmatched = [r for r in ing if r.matched_declared is None]
    ctx.facts["label_ingredients"] = len(ing)
    ctx.facts["label_ingredients_unmatched"] = len(unmatched)
    actives, inactives = [], []
    for r in unmatched:
        (actives if row_is_active(ref, r) else inactives).append(r)
    for r in actives:
        el = ref.get(r.resolution.uid)
        conf = (r.resolution.confidence if el else 0.6) * (1.0 if r.grounded else 0.6)
        what = el.label() if el else "absent du référentiel"
        ctx.add(
            "R-ING-ACTIVE",
            Severity.MAJOR,
            FraudType.undeclared_ingredients,
            conf,
            f"Ingrédient actif de l'étiquette non déclaré : {r.raw}",
            f"« {r.raw} » figure sur l'étiquette ({what}) mais n'apparaît pas dans la composition déclarée.",
            [Evidence(quote=r.raw, page=r.page)],
            r.grounded,
            [r.resolution.uid] if r.resolution.uid else [],
        )
    for r in inactives:
        el = ref.get(r.resolution.uid)
        ctx.add(
            "R-ING-INACTIVE",
            Severity.MINOR,
            FraudType.undeclared_ingredients,
            (r.resolution.confidence if el else 0.5) * (1.0 if r.grounded else 0.6),
            f"Ingrédient non actif de l'étiquette non déclaré : {r.raw}",
            f"« {r.raw} » ({el.label() if el else 'non identifié'}) est sur l'étiquette mais pas dans la déclaration.",
            [Evidence(quote=r.raw, page=r.page)],
            r.grounded,
            [r.resolution.uid] if r.resolution.uid else [],
        )
    n, k = len(ing), len(unmatched)
    grounded_share = sum(1 for r in unmatched if r.grounded) / max(k, 1)
    if k >= 4 and k / n >= 0.5:
        ctx.add(
            "R-ING-MASSIVE",
            Severity.BLOCKING,
            FraudType.undeclared_ingredients,
            min(0.95, 0.6 + 0.35 * grounded_share),
            "Une grande partie des ingrédients de l'étiquette n'est pas déclarée",
            f"{k} ingrédients sur {n} lus sur l'étiquette ne figurent pas dans la déclaration : "
            + ", ".join(f"« {r.raw} »" for r in unmatched[:12])
            + ".",
            [Evidence(quote=r.raw, page=r.page) for r in unmatched[:6]],
        )
    elif k >= 3 and k / n >= 0.3:
        ctx.add(
            "R-ING-MANY",
            Severity.MAJOR,
            FraudType.undeclared_ingredients,
            0.5 + 0.4 * grounded_share,
            "Plusieurs ingrédients de l'étiquette ne sont pas déclarés",
            f"{k} ingrédients sur {n} non déclarés : " + ", ".join(f"« {r.raw} »" for r in unmatched[:12]) + ".",
            [Evidence(quote=r.raw, page=r.page) for r in unmatched[:6]],
        )


# =============================================================================== R-DOSE
def _units_per_day(ctx: Context) -> tuple[float | None, str]:
    """Max units per day, from the label first, else from the declared daily dose. Returns (value, source)."""
    dd = ctx.label.first(lambda e: e.daily_dose.units_per_day_max)
    if dd:
        return float(dd), "étiquette"
    m = re.search(r"(\d+(?:[.,]\d+)?)", ctx.decl.daily_recommended_dose or "")
    if m:
        return float(m.group(1).replace(",", ".")), "déclaration"
    return None, ""


# Nutrient reference values (INCO regulation 1169/2011, annex XIII): (name pattern, value, unit)
NRV = [
    (r"vitamine a\b|retinol", 800, "µg"), (r"vitamine d", 5, "µg"), (r"vitamine e\b|tocopher", 12, "mg"),
    (r"vitamine k", 75, "µg"), (r"vitamine c\b|ascorbi", 80, "mg"), (r"vitamine b1\b|thiamin", 1.1, "mg"),
    (r"vitamine b2|riboflavin", 1.4, "mg"), (r"vitamine b3|niacin|nicotinam", 16, "mg"), (r"vitamine b6|pyridox", 1.4, "mg"),
    (r"vitamine b9|folat|acide folique", 200, "µg"), (r"vitamine b12|cobalamin", 2.5, "µg"), (r"biotine|vitamine b8", 50, "µg"),
    (r"vitamine b5|pantoth", 6, "mg"), (r"potassium", 2000, "mg"), (r"calcium", 800, "mg"), (r"phosphore", 700, "mg"),
    (r"magnesium", 375, "mg"), (r"\bfer\b", 14, "mg"), (r"\bzinc\b", 10, "mg"), (r"cuivre", 1, "mg"),
    (r"manganese", 2, "mg"), (r"selenium", 55, "µg"), (r"chrome\b", 40, "µg"), (r"molybden", 50, "µg"), (r"\biode\b", 150, "µg"),
]  # fmt: skip


def nrv_consistent(name: str, value: float | None, unit: str | None, nrv_percent: float | None) -> bool | None:
    """Check that a quantity and its %NRV are consistent for the named substance.

    An inconsistency almost always means a misreading (e.g. "Magnesium 56 mg (15 %)" read as
    "Manganese 56 mg (150 %)"). Returns None when no conclusion is possible.
    """
    if value is None or not nrv_percent or nrv_percent <= 0:
        return None
    n = normalise(name)
    for pattern, ref, ref_unit in NRV:
        if re.search(pattern, n):
            q = convert(value, unit, ref_unit)
            if q is None:
                return None
            implied = 100 * q / ref
            return 0.6 <= implied / nrv_percent <= 1.6
    return None


def label_quantities(ctx: Context) -> list[dict]:
    """Daily quantities read on the label, resolved and converted into the element's unit.

    Each entry carries a `certainty` (0-1) that reflects how the daily amount was derived:
    1.0 for an explicit per-daily-dose value, lower when it had to be computed or guessed.
    """
    ref = ctx.ref
    upd, upd_src = _units_per_day(ctx)
    out = []
    for r in ctx.composition_rows:
        row = r.row
        el = ref.get(r.resolution.uid)
        if el is None or row.value is None or r.resolution.confidence < RESOLUTION_MIN_CONF:
            continue
        if EQUIVALENCE.search(normalise(row.raw)) or EQUIVALENCE.search(normalise(row.basis_text)):
            continue
        basis_txt = normalise(row.basis_text)
        certainty = 1.0
        if row.basis == Basis.per_daily_dose or re.search(r"\b(jour|djr|quotidien|journaliere)\b", basis_txt):
            q = row.value
        elif row.basis == Basis.per_unit:
            if upd is None:
                continue
            m = re.search(r"pour (\d+)", basis_txt)  # "pour 2 gélules"
            per = float(m.group(1)) if m else 1.0
            q = row.value * upd / per
            certainty = 0.85 if upd_src == "étiquette" else 0.7
        elif row.basis == Basis.per_serving:
            q, certainty = row.value, 0.6
        elif row.basis == Basis.unknown:
            q, certainty = row.value, 0.65
        else:  # per 100 g/ml: cannot be converted without the daily mass
            continue
        target_unit = ref.unit_name(el.unit_id) or row.unit
        qv = convert(q, row.unit, target_unit, el.name)
        if qv is None:
            continue
        coherent = nrv_consistent(el.name, row.value, row.unit, row.nrv_percent)
        if coherent is False:
            certainty *= 0.2  # reading inconsistent with its %NRV: unusable for blocking
        out.append(
            {
                "row": r,
                "uid": el.uid,
                "quantity": qv,
                "unit": target_unit,
                "certainty": certainty,
                "label_text": row.raw,
                "page": r.page,
            }
        )
    return out


def rule_doses(ctx: Context) -> None:
    """Compare label daily quantities with the max doses (per population) and the declared quantities.

    A label dose above the max while the declaration stays below it is a hidden overdose (BLOCKING):
    the declarant under-declared to stay in article 15.
    """
    ref, decl = ctx.ref, ctx.decl
    declared_q: dict[str, tuple[float, int | None]] = {}
    for c in decl.computed_substances:
        if c.quantity is not None:
            declared_q[c.uid] = (c.quantity, c.unit_id)
    for it in decl.items:
        if it.uid and it.quantity is not None and it.uid not in declared_q:
            declared_q[it.uid] = (it.quantity, it.unit_id)
    qs = label_quantities(ctx)
    ctx.facts["label_quantities"] = len(qs)
    for q in qs:
        el = ref.get(q["uid"])
        mx = ref.max_for(el, decl.populations)
        dq = declared_q.get(q["uid"])
        conf_base = q["certainty"] * q["row"].resolution.confidence * (1.0 if q["row"].grounded else 0.6)
        ev = [Evidence(quote=q["label_text"], page=q["page"])]
        declared_conv = convert(dq[0], ref.unit_name(dq[1]) or q["unit"], q["unit"], el.name) if dq else None
        if mx is not None and q["quantity"] > mx * (1 + 1e-6):
            if declared_conv is None or declared_conv <= mx:
                ctx.add(
                    "R-DOSE-OVERMAX-HIDDEN",
                    Severity.BLOCKING,
                    FraudType.dose_underdeclared,
                    conf_base,
                    f"Dose de l'étiquette au-delà du maximum autorisé : {el.name}",
                    f"L'étiquette indique {q['quantity']:g} {q['unit']} de {el.name} par jour (« {q['label_text']} »), "
                    f"au-delà de la dose maximale de {mx:g} {q['unit']}"
                    + (
                        f", alors que la déclaration indique {declared_conv:g} {q['unit']}."
                        if declared_conv is not None
                        else ", et aucune quantité n'est déclarée."
                    ),
                    ev,
                    q["row"].grounded,
                    [el.uid],
                )
                continue
        if declared_conv is not None and declared_conv > 0:
            ratio = q["quantity"] / declared_conv
            if ratio > 1 + DOSE_TOLERANCE:
                near_max = mx is not None and q["quantity"] >= 0.9 * mx
                ctx.add(
                    "R-DOSE-HIGHER",
                    Severity.MAJOR,
                    FraudType.dose_underdeclared,
                    conf_base * (1.0 if ratio > 1.25 else 0.8),
                    f"Quantité de l'étiquette supérieure à la déclaration : {el.name}",
                    f"L'étiquette indique {q['quantity']:g} {q['unit']} par jour, la déclaration {declared_conv:g} {q['unit']} "
                    f"(×{ratio:.2f})" + (f" ; proche du maximum de {mx:g} {q['unit']}." if near_max else "."),
                    ev,
                    q["row"].grounded,
                    [el.uid],
                )
            elif ratio < 1 - DOSE_TOLERANCE:
                ctx.add(
                    "R-DOSE-LOWER",
                    Severity.MINOR,
                    FraudType.label_noncompliance,
                    conf_base * 0.8,
                    f"Quantité de l'étiquette inférieure à la déclaration : {el.name}",
                    f"L'étiquette indique {q['quantity']:g} {q['unit']}, la déclaration {declared_conv:g} {q['unit']}.",
                    ev,
                    q["row"].grounded,
                    [el.uid],
                )
    ctx.facts["_label_quantities"] = qs  # reused by rule_counterfactual_article


# =============================================================================== R-ART
def rule_counterfactual_article(ctx: Context) -> None:
    """Recompute the article with what the label really contains (undeclared elements and label
    quantities added to the declared composition). If the label leads out of article 15 while the
    declaration is in article 15, the declarant bypassed the procedure: BLOCKING.

    Must run after rule_doses (it reuses ctx.facts["_label_quantities"]).
    """
    ref, decl = ctx.ref, ctx.decl
    base = composition_from_declaration(decl, ref)
    declared_res = compute_article(base, ref)
    declared_article = decl.article or declared_res.article
    ctx.facts["declared_article"] = declared_article
    # What the label adds to the declared composition: (kind, object, label row) triples.
    additions: list[tuple[str, object, LabelRow]] = []
    for r in ctx.ingredient_rows:
        if r.matched_declared is not None:
            continue
        el = ref.get(r.resolution.uid)
        if el and r.resolution.confidence >= RESOLUTION_MIN_CONF:
            additions.append(
                ("item", CompItem(kind=el.kind, uid=el.uid, used_part_id=r.resolution.part_id, source="label"), r)
            )
        # An active ingredient that is not in the reference data at all would make it a "new
        # ingredient" (ART_16), but only when the reading is solid: grounded, high confidence,
        # not a generic header and not part of a premix.
        elif (
            el is None
            and r.ingredient
            and row_is_active(ref, r)
            and r.resolution.method == "none"
            and r.resolution.confidence >= 0.85
            and r.grounded
            and not is_generic(r)
            and not r.ingredient.from_premix
        ):
            additions.append(("item", CompItem(kind="ingredient", uid=None, new=True, source="label"), r))
    for q in ctx.facts.get("_label_quantities", []):
        el = ref.get(q["uid"])
        if el.kind == "substance":
            additions.append(("subst", CompSubstance(uid=el.uid, quantity=q["quantity"], source="label"), q["row"]))

    def build(extra) -> Composition:
        """Declared composition + `extra` additions. A label quantity replaces a lower declared one."""
        comp = composition_from_declaration(decl, ref)
        for kind, obj, _ in extra:
            if kind == "item":
                comp.items.append(obj)
            else:
                existing = next((s for s in comp.computed_substances if s.uid == obj.uid), None)
                if existing:
                    if existing.quantity is None or (obj.quantity or 0) > existing.quantity:
                        existing.quantity = obj.quantity
                else:
                    comp.computed_substances.append(obj)
        return comp

    cf = compute_article(build(additions), ref)
    ctx.facts["counterfactual_article"] = cf.article
    ctx.facts["counterfactual_reasons"] = cf.reasons
    # "Declared composition" and "label composition" are compared under the SAME reference data:
    # if the reference data changed since the declaration, the gap must not be blamed on the label.
    baseline = declared_res.article if declared_res.article is not None else declared_article
    ctx.facts["declared_article_recomputed"] = declared_res.article
    if not additions or RANK.get(cf.article, 0) <= max(RANK.get(baseline, 0), 0):
        return
    # Which additions, taken one at a time, are enough to escalate the article (the actual causes).
    causes = []
    for a in additions:
        single = compute_article(build([a]), ref)
        if RANK.get(single.article, 0) > RANK.get(baseline, 0):
            causes.append((a, single))
    causes = causes or [(a, cf) for a in additions]
    conf = max(
        (c[0][2].resolution.confidence if c[0][2].resolution.uid else c[0][2].resolution.confidence * 0.8)
        * (1.0 if c[0][2].grounded else 0.6)
        for c in causes
    )
    ev = [Evidence(quote=c[0][2].raw, page=c[0][2].page) for c in causes[:5]]
    detail = (
        f"Article déclaré : {declared_article}. Avec la composition réellement lue sur l'étiquette, l'article "
        f"serait {cf.article} ({'; '.join(cf.reasons)}). Éléments en cause : "
        + ", ".join(f"« {c[0][2].raw} »" for c in causes[:6])
        + "."
    )
    if declared_article in AUTO_VALIDABLE and cf.article not in AUTO_VALIDABLE:
        ctx.add(
            "R-ART-BYPASS",
            Severity.BLOCKING,
            FraudType.article_bypass,
            conf,
            f"Contournement de l'article 15 : l'étiquette relève de l'{cf.article}",
            detail,
            ev,
            all(c[0][2].grounded for c in causes),
            [c[0][1].uid for c in causes if getattr(c[0][1], "uid", None)],
        )
    elif declared_article == ART_15 and cf.article == ART_15_WARNING:
        ctx.add(
            "R-ART-WARNING",
            Severity.MAJOR,
            FraudType.article_bypass,
            conf * 0.9,
            "Ingrédient « à surveiller » présent sur l'étiquette mais non déclaré",
            detail,
            ev,
        )
    else:
        ctx.add(
            "R-ART-ESCALATION",
            Severity.MAJOR,
            FraudType.article_bypass,
            conf * 0.9,
            f"L'étiquette implique un article plus contraignant ({cf.article})",
            detail,
            ev,
        )


# =============================================================================== R-MEN
MENTION_RULES = {
    # key: (French title, severity, double-check regexes on the normalised OCR text)
    "denomination_complement_alimentaire": (
        "Dénomination « complément alimentaire »",
        Severity.MAJOR,
        [r"complements? alimentaires?", r"food supplement", r"nahrungserganzungsmittel"],
    ),
    "daily_dose": (
        "Portion journalière recommandée",
        Severity.MAJOR,
        [r"par jour", r"\bjour\b", r"quotidien", r"posologie", r"conseils? d (utilisation|emploi)", r"mode d emploi"],
    ),
    "warning_do_not_exceed": (
        "« Ne pas dépasser la dose journalière recommandée »",
        Severity.MAJOR,
        [r"ne pas depasser", r"ne depassez pas"],
    ),
    "warning_varied_diet": (
        "Mention « ne se substitue pas à un régime alimentaire varié »",
        Severity.MAJOR,
        [r"(regime|alimentation) (alimentaire )?(varie|equilibre)", r"substitu", r"mode de vie sain"],
    ),
    "warning_children": (
        "« Tenir hors de la portée des jeunes enfants »",
        Severity.MAJOR,
        [r"(portee|vue|atteinte|l abri).{0,30}enfants", r"tenir hors"],
    ),
    "quantities_per_daily_dose": ("Quantités des actifs par DJR (art. 12-I)", Severity.MAJOR, []),
    "ingredients_list": ("Liste des ingrédients", Severity.MAJOR, [r"\bingredients?\b", r"\bcomposition\b"]),
    "net_quantity": (
        "Quantité nette",
        Severity.MINOR,
        [r"poids net", r"contenance", r"quantite nette", r"\bnet\b", r"\d+ ?(gelules|comprimes|capsules|g|ml)\b"],
    ),
    "best_before": (
        "Date de durabilité minimale",
        Severity.MINOR,
        [r"a consommer de preference", r"\bddm\b", r"\bdluo\b", r"a consommer avant", r"best before", r"\bexp\b"],
    ),
    "lot": ("Numéro de lot", Severity.MINOR, [r"\blot\b", r"\bbatch\b"]),
    "operator": (
        "Nom et adresse de l'exploitant",
        Severity.MINOR,
        [
            r"\b\d{5}\b",
            r"\bsas\b",
            r"\bsarl\b",
            r"laboratoire",
            r"distribue par",
            r"fabrique (par|pour)",
            r"\bfrance\b",
        ],
    ),
}
# The five statements every genuine French label carries. Three or more missing = fake label.
CORE_MENTIONS = [
    "denomination_complement_alimentaire",
    "daily_dose",
    "warning_do_not_exceed",
    "warning_varied_diet",
    "warning_children",
]


def rule_mentions(ctx: Context) -> None:
    """Mandatory statements. "Absent" is only kept when BOTH the model and a regex search of the
    label text fail to find the statement (the model misses reworded or small-print statements)."""
    text = ctx.label.text
    legibility = {f.extraction.legibility.value for f in ctx.label.files}
    leg_factor = 1.0 if "good" in legibility else 0.75 if "partial" in legibility else 0.5
    missing_core = []
    for key, (title, sev, patterns) in MENTION_RULES.items():
        m, fi = ctx.label.mention(key)
        if key == "quantities_per_daily_dose":
            # Art. 12-I: EVERY declared active ingredient must have its daily quantity on the label
            missing_qty = []
            for i, it in enumerate(ctx.decl.items):
                el = ctx.ref.get(it.uid)
                if not it.active or (el and not el.active):
                    continue
                has_qty = any(
                    r.matched_declared == i
                    and (
                        (r.kind == "composition" and r.row.value is not None)
                        or (r.kind == "ingredient" and r.ingredient.quantity is not None)
                    )
                    for r in ctx.rows
                )
                if not has_qty:
                    missing_qty.append(it.name)
            ctx.facts["actives_without_label_quantity"] = missing_qty
            if not missing_qty:
                continue
            # When there is a table, the gap may come from a failed match: lower confidence
            conf = (0.8 if not ctx.composition_rows else 0.65) * leg_factor
            ctx.add(
                f"R-MEN-{key}",
                sev,
                FraudType.label_noncompliance,
                conf,
                f"Mention obligatoire absente : {title}",
                "Quantité par DJR absente de l'étiquette pour : " + ", ".join(missing_qty[:8]) + ".",
            )
            continue
        else:
            if m.status != MentionStatus.absent:
                continue
            hit = contains_any(text, patterns) if patterns else None
            if hit:  # the OCR text contains the statement: do not trust the model's "absent"
                continue
            conf = 0.85 * leg_factor
        if key in CORE_MENTIONS:
            missing_core.append(title)
        ctx.add(
            f"R-MEN-{key}",
            sev,
            FraudType.label_noncompliance,
            conf,
            f"Mention obligatoire absente : {title}",
            f"La mention {title} n'a été trouvée ni par la lecture de l'étiquette ni dans sa transcription.",
        )
    ctx.facts["missing_core_mentions"] = missing_core
    if len(missing_core) >= 3:
        ctx.add(
            "R-MEN-FAKE",
            Severity.BLOCKING,
            FraudType.fake_label,
            min(0.95, (0.6 + 0.1 * len(missing_core)) * leg_factor),
            "Étiquette sans les mentions obligatoires de base",
            f"{len(missing_core)} mentions obligatoires de base sont absentes : " + "; ".join(missing_core) + ".",
        )


# =============================================================================== R-DOC
# Only unambiguous signals: not the OCR's markdown image links ("[img-0.jpeg]"), nor "Lot : XXX",
# which is a placeholder for a value printed at packing time.
PLACEHOLDER = re.compile(r"lorem ipsum|nom du produit|a completer|texte a venir|placeholder|votre texte ici", re.I)


def rule_document(ctx: Context) -> None:
    """The file itself: not a label, placeholder text, illegible, no French."""
    files = ctx.label.files
    non_labels = [
        f
        for f in files
        if not f.extraction.is_food_supplement_label
        or f.extraction.document_kind.value in ("text_document", "form_screenshot", "technical_sheet", "other")
    ]
    if files and len(non_labels) == len(files):
        kinds = ", ".join(sorted({f.extraction.document_kind.value for f in non_labels}))
        ctx.add(
            "R-DOC-NOT-LABEL",
            Severity.BLOCKING,
            FraudType.fake_label,
            0.85,
            "Le document fourni n'est pas une étiquette",
            f"Aucun des fichiers fournis comme étiquetage n'est une étiquette ou une maquette d'emballage ({kinds}).",
        )
    anomalies = [a for f in files for a in f.extraction.anomalies]
    placeholders = [a for a in anomalies if PLACEHOLDER.search(normalise(a))] + PLACEHOLDER.findall(
        normalise(ctx.label.text)
    )[:3]
    if placeholders:
        ctx.add(
            "R-DOC-PLACEHOLDER",
            Severity.BLOCKING if len(placeholders) >= 2 else Severity.MAJOR,
            FraudType.fake_label,
            0.8,
            "Texte de remplissage sur l'étiquette",
            "Éléments relevés : " + "; ".join(map(str, placeholders[:5])),
            grounded_=bool(PLACEHOLDER.findall(normalise(ctx.label.text))),
        )
    elif anomalies:
        ctx.add(
            "R-DOC-ANOMALY",
            Severity.MINOR,
            FraudType.fake_label,
            0.5,
            "Anomalies relevées sur l'étiquette",
            "; ".join(anomalies[:5]),
        )
    if files and all(f.extraction.legibility.value == "poor" for f in files):
        ctx.add(
            "R-DOC-ILLEGIBLE",
            Severity.BLOCKING,
            FraudType.label_noncompliance,
            0.8,
            "Étiquette illisible",
            "L'étiquette fournie n'est pas lisible : sa conformité ne peut pas être vérifiée.",
        )
    if files and not any(f.extraction.french_present for f in files):
        # double-check on the text before concluding that there is no French at all
        fr = contains_any(
            ctx.label.text, [r"complement alimentaire", r"\bingredients?\b.*\b(de|et)\b", r"ne pas depasser"]
        )
        if not fr:
            ctx.add(
                "R-DOC-NO-FRENCH",
                Severity.BLOCKING,
                FraudType.label_noncompliance,
                0.85,
                "Étiquetage non rédigé en français",
                "Les mentions obligatoires doivent être rédigées en français (art. R. 412-7 du code de la consommation).",
            )


# =============================================================================== R-ID
def rule_identity(ctx: Context) -> None:
    """Is this the label of the declared product? Coverage of the declared actives, name and brand."""
    decl, text = ctx.decl, ctx.label.text
    name_score = quote_in_text(decl.name, text) if decl.name else 100.0
    brand_score = quote_in_text(decl.brand, text) if decl.brand else 100.0
    actives = [i for i, it in enumerate(decl.items) if it.active]
    matched = {r.matched_declared for r in ctx.rows if r.matched_declared is not None}
    coverage = len([i for i in actives if i in matched]) / len(actives) if actives else 1.0
    ctx.facts.update(
        {"name_score": name_score, "brand_score": brand_score, "declared_active_coverage": round(coverage, 2)}
    )
    if len(actives) >= 2 and coverage < 0.34 and ctx.ingredient_rows:
        conf = 0.75 + (0.15 if name_score < 60 else 0.0)
        missing = [decl.items[i].name for i in actives if i not in matched]
        ctx.add(
            "R-ID-OTHER-PRODUCT",
            Severity.BLOCKING,
            FraudType.fake_label,
            conf,
            "L'étiquette ne correspond pas à la composition déclarée",
            f"Seuls {coverage:.0%} des ingrédients actifs déclarés se retrouvent sur l'étiquette. Absents : "
            + ", ".join(missing[:10])
            + "."
            + (" Le nom du produit n'apparaît pas non plus." if name_score < 60 else ""),
        )
    elif name_score < 60 and brand_score < 60 and decl.name:
        ctx.add(
            "R-ID-NAME",
            Severity.MAJOR,
            FraudType.fake_label,
            0.6,
            "Nom et marque du produit absents de l'étiquette",
            f"Ni « {decl.name} » ni la marque « {decl.brand} » ne figurent sur l'étiquette.",
        )
    # Informational only (does not block): kept in the trace to help diagnose reading problems.
    missing_declared = [decl.items[i] for i in actives if i not in matched]
    for it in missing_declared[:10]:
        ctx.add(
            "R-ID-DECLARED-NOT-ON-LABEL",
            Severity.INFO,
            FraudType.label_noncompliance,
            0.5,
            f"Ingrédient déclaré non retrouvé sur l'étiquette : {it.name}",
            "Peut signaler une étiquette d'un autre produit, ou un défaut de lecture.",
        )


# =============================================================================== R-DJR
def _max_number(text: str) -> float | None:
    nums = [float(n.replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", text or "")]
    return max(nums) if nums else None


def rule_daily_dose(ctx: Context) -> None:
    """The label's daily dose (max units per day) must not exceed the declared one: if it does,
    every declared per-day quantity is under-estimated."""
    label_upd = ctx.label.first(lambda e: e.daily_dose.units_per_day_max)
    label_text = ctx.label.first(lambda e: e.daily_dose.text)
    declared = _max_number(ctx.decl.daily_recommended_dose)
    if not label_upd or not declared or not label_text:
        return
    # Only compare doses expressed in comparable units (same unit keyword on both sides)
    unit_words = r"(gelule|comprime|capsule|goutte|sachet|ampoule|ml|cuillere|pastille|gomme|stick|dose|mesure)"
    lu = re.search(unit_words, normalise(label_text))
    du = re.search(unit_words, normalise(ctx.decl.daily_recommended_dose))
    if not lu or not du or lu.group(1) != du.group(1):
        return
    if abs(label_upd - declared) > 1e-6 and label_upd > declared:
        page = ctx.label.first(lambda e: e.daily_dose.page) or 0
        ctx.add(
            "R-DJR-HIGHER",
            Severity.MAJOR,
            FraudType.dose_underdeclared,
            0.8 if grounded(label_text, ctx.label.text) else 0.5,
            "Dose journalière de l'étiquette supérieure à la déclaration",
            f"Étiquette : « {label_text} » (jusqu'à {label_upd:g} par jour). Déclaration : « {ctx.decl.daily_recommended_dose} ». "
            "Les quantités déclarées par DJR sont donc sous-estimées.",
            [Evidence(quote=label_text, page=page)],
            grounded(label_text, ctx.label.text),
        )


def rule_drops_in_ml(ctx: Context) -> None:
    """Instructor doctrine: a daily dose in drops must also be expressed as a volume (ml) on the label."""
    text = ctx.label.first(lambda e: e.daily_dose.text) or ""
    n = normalise(text)
    if re.search(r"\bgouttes?\b", n) and not re.search(r"\bml\b|millilitre", n):
        dd_page = ctx.label.first(lambda e: e.daily_dose.page) or 0
        whole = normalise(ctx.label.text)
        # the volume may be written elsewhere on the label, next to the number of drops
        if not re.search(r"gouttes?\D{0,25}\d+([.,]\d+)? ?ml|\d+([.,]\d+)? ?ml\D{0,25}gouttes?", whole):
            ctx.add(
                "R-DJR-DROPS-ML",
                Severity.MAJOR,
                FraudType.label_noncompliance,
                0.8,
                "DJR en gouttes non exprimée en volume",
                f"La posologie « {text} » est exprimée en gouttes : la dose journalière doit aussi figurer en ml.",
                [Evidence(quote=text, page=dd_page)],
                grounded(text, ctx.label.text),
            )


# Alcohol in the product (label wording or declared preparation), and the matching warning.
ALCOHOL = re.compile(r"\b(alcool|ethanol|alcohol|teinture|eau de vie|spiritueux)\b")
ALCOHOL_WARNING = re.compile(
    r"(deconseill|ne convient pas|interdit|ne pas (donner|administrer)|reserve aux adultes|"
    r"pas recommande).{0,80}(enfant|moins de 1[28]|femmes? enceinte|grossesse)|"
    r"(enfant|moins de 1[28]|femmes? enceinte).{0,60}(deconseill|ne convient pas|interdit)"
)


def rule_alcohol_warning(ctx: Context) -> None:
    """Instructor doctrine: alcohol requires a warning (children, pregnant women)."""
    in_label = [r for r in ctx.ingredient_rows if ALCOHOL.search(normalise(r.raw))]
    in_decl = [
        it
        for it in ctx.decl.items
        if ALCOHOL.search(normalise(it.name))
        or (it.preparation_id and ctx.ref.preparations.get(str(it.preparation_id), {}).get("contains_alcohol"))
    ]
    if not (in_label or in_decl):
        return
    warnings_text = " ".join(normalise(w.quote) for _, w in ctx.label.warnings()) + " " + normalise(ctx.label.text)
    if ALCOHOL_WARNING.search(warnings_text):
        return
    ev = [Evidence(quote=r.raw, page=r.page) for r in in_label[:2]]
    ctx.add(
        "R-WARN-ALCOHOL",
        Severity.MAJOR,
        FraudType.label_noncompliance,
        0.8 if in_label else 0.65,
        "Présence d'alcool sans avertissement pour les enfants / femmes enceintes",
        "Le produit contient de l'alcool ("
        + ", ".join([r.raw for r in in_label[:2]] + [it.name for it in in_decl[:2]])
        + ") mais l'étiquette ne le déconseille pas aux enfants ni aux femmes enceintes.",
        ev,
        bool(ev),
    )


# =============================================================================== R-CLM
# "cures / treats <disease>": a food supplement cannot claim to prevent, treat or cure a disease.
THERAPEUTIC = re.compile(
    r"\b(guerit|guerir|guerison|soigne|soigner|traite|traiter|traitement)\b.{0,50}\b(maladie|cancer|diabete|depression|"
    r"infection|alzheimer|hypertension|arthrose|cholesterol|tumeur|covid|grippe)",
    re.I,
)


def rule_claims(ctx: Context) -> None:
    for fi, c in ctx.label.claims():
        if THERAPEUTIC.search(normalise(c.quote)):
            ctx.add(
                "R-CLM-THERAPEUTIC",
                Severity.MAJOR,
                FraudType.label_noncompliance,
                0.75,
                "Allégation thérapeutique",
                f"« {c.quote} » : un complément alimentaire ne peut pas revendiquer "
                "de prévenir, traiter ou guérir une maladie.",
                [c],
                grounded(c.quote, ctx.label.text),
            )


# =============================================================================== R-WARN
# Words too common in regulatory warnings to identify one (normalised French).
WARNING_STOPWORDS = {
    "etiquetage", "comporter", "avertissement", "deconseille", "deconseillee", "deconseilles", "emploi", "personnes",
    "utilisation", "produit", "produits", "complement", "complements", "alimentaire", "alimentaires", "consommation",
    "medical", "medicale", "professionnel", "conseil", "information", "concernant", "contenant", "preparation",
    "devrait", "mention", "presence", "encadrement", "supplementation", "apport", "risques", "population",
}  # fmt: skip


def warning_keywords_present(warning: str, label_text: str, share: float = 0.6) -> bool:
    """Are the distinctive words of a regulatory warning ("crustacés", "anticoagulant",
    "diabétiques"...) present in the label text? Tolerates rewording (6-letter prefix match)."""
    words = {w for w in normalise(warning).split() if len(w) >= 6 and w not in WARNING_STOPWORDS}
    if len(words) < 2:
        return False
    text_prefixes = {t[:6] for t in normalise(label_text).split() if len(t) >= 6}
    hits = sum(1 for w in words if w[:6] in text_prefixes)
    return hits / len(words) >= share


async def rule_specific_warnings(ctx: Context, client: LLMClient) -> None:
    """Warnings made mandatory by the ingredients (reference data `warnings_on_label`), for the
    declared elements and the elements read on the label.

    A small model judges whether each required warning is present, even reworded. An "absent"
    is then double-checked with warning_keywords_present before raising a finding.
    """
    ref = ctx.ref
    uids = {it.uid for it in ctx.decl.items if it.uid} | {
        r.resolution.uid
        for r in ctx.ingredient_rows
        if r.resolution.uid and r.resolution.confidence >= RESOLUTION_MIN_CONF
    }
    required: list[tuple[str, str]] = []  # (element name, warning text), de-duplicated
    seen = set()
    for uid in sorted(uids):
        el = ref.get(uid)
        for w in el.warnings if el else []:
            k = normalise(w)
            if k and k not in seen:
                seen.add(k)
                required.append((el.name, w))
    ctx.facts["required_specific_warnings"] = len(required)
    if not required:
        return
    label_warnings = "\n".join(f"- (p.{w.page}) {w.quote}" for _, w in ctx.label.warnings())
    # Model input (French keys, like the prompt).
    payload = {
        "avertissements_requis": [{"index": i, "ingredient": n, "texte": w} for i, (n, w) in enumerate(required)],
        "avertissements_de_l_etiquette": label_warnings[:8000],
        "transcription_complete": ctx.label.text[:30000],
    }
    out: WarningCheck = await client.chat_json(
        "check_warnings",
        ctx.settings.model_check,
        [
            {"role": "system", "content": prompt_text("check_warnings.md")},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        WarningCheck,
        max_tokens=3000,
        cache_parts={"prompt": prompt_hash("check_warnings.md"), "payload": payload},
    )
    legible = any(f.extraction.legibility.value != "poor" for f in ctx.label.files)
    for item in out.items:
        if item.index >= len(required) or item.status == "present":
            continue
        name, w = required[item.index]
        if warning_keywords_present(w, ctx.label.text):
            continue  # double-check: the warning's distinctive words are in the label text
        sev = Severity.MAJOR if item.status == "absent" else Severity.MINOR
        ctx.add(
            "R-WARN-MISSING",
            sev,
            FraudType.label_noncompliance,
            (0.8 if item.status == "absent" else 0.5) * (1 if legible else 0.6),
            f"Avertissement obligatoire absent ({name})",
            f"La présence de {name} impose l'avertissement : « {w} ». Il n'a pas été trouvé sur l'étiquette"
            + (" (seulement partiellement)." if item.status == "partial" else "."),
            [Evidence(quote=item.quote, page=item.page or 0)] if item.quote else [],
        )
