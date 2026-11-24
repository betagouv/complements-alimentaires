"""Rules engine (rules.py) and decision (decision.py) on synthetic labels."""

from ai_v2.config import Settings
from ai_v2.decision import decide, risk_score
from ai_v2.rules import (
    Context,
    LabelRow,
    match_rows_to_declaration,
    rule_completeness,
    rule_counterfactual_article,
    rule_document,
    rule_doses,
    rule_mentions,
)
from ai_v2.schemas import Basis, DocumentKind, Finding, FraudType, Severity

from .factories import comp_row, computed, declaration, ingredient, item, label, mention, mentions, refdata, resolution

REF = refdata()
S = Settings()


def ctx_for(decl, lab, resolutions):
    rows = []
    ings = lab.ingredients()
    comps = lab.composition()
    for (fi, i, g), res in zip(ings, resolutions[: len(ings)]):
        rows.append(LabelRow(fi, "ingredient", i.raw, i.name, i.page, g, res, ingredient=i))
    for (fi, r, g), res in zip(comps, resolutions[len(ings) :]):
        rows.append(LabelRow(fi, "composition", r.raw, r.name, r.page, g, res, row=r))
    c = Context(settings=S, ref=REF, decl=decl, label=lab, rows=rows)
    match_rows_to_declaration(c)
    return c


def codes(c):
    return {f.code for f in c.findings}


def test_counterfactual_article_bypass_detected():
    decl = declaration([item("plant", "plant:1", "Curcuma longa L.", 300)])
    lab = label([ingredient("extrait de curcuma"), ingredient("Ephedra sinica")])
    c = ctx_for(decl, lab, [resolution("extrait de curcuma", "plant:1"), resolution("Ephedra sinica", "plant:2")])
    rule_completeness(c)
    rule_counterfactual_article(c)
    assert "R-ART-BYPASS" in codes(c)
    assert c.facts["counterfactual_article"] == "ART_16"
    f = next(f for f in c.findings if f.code == "R-ART-BYPASS")
    assert f.severity == Severity.BLOCKING and f.grounded and "Ephedra" in f.detail


def test_counterfactual_ignores_refdata_drift_and_empty_additions():
    # stored article ART_15, but the current reference data classifies the declared plant as not authorised:
    # the gap comes from the reference data, not from the label -> no finding, and above all no crash
    decl = declaration([item("plant", "plant:2", "Ephedra sinica Stapf", 100)], article="ART_15")
    lab = label([ingredient("Ephedra sinica")])
    c = ctx_for(decl, lab, [resolution("Ephedra sinica", "plant:2")])
    rule_counterfactual_article(c)
    assert not [f for f in c.findings if f.code.startswith("R-ART")]


def test_substance_matches_its_declared_form_of_supply():
    decl = declaration(
        [item("ingredient", "ingredient:21", "gluconate de zinc", 70)], [computed("substance:10", "zinc", 10)]
    )
    lab = label([ingredient("gluconate de zinc")], [comp_row("Zinc 10 mg", "zinc", 10, "mg")])
    c = ctx_for(decl, lab, [resolution("gluconate de zinc", "ingredient:21"), resolution("zinc", "substance:10")])
    rule_completeness(c)
    rule_doses(c)
    assert not [f for f in c.findings if f.code.startswith(("R-ING", "R-DOSE"))]


def test_hidden_overdose_per_unit_times_units_per_day():
    # 10 mg of zinc PER CAPSULE x 2 capsules/day = 20 mg > 15 mg max, declared 10 mg
    decl = declaration(
        [item("ingredient", "ingredient:21", "gluconate de zinc", 70)], [computed("substance:10", "zinc", 10)]
    )
    lab = label(
        [ingredient("gluconate de zinc")],
        [comp_row("Zinc 10 mg", "zinc", 10, "mg", basis=Basis.per_unit, basis_text="par gélule")],
        units_per_day=2,
    )
    c = ctx_for(decl, lab, [resolution("gluconate de zinc", "ingredient:21"), resolution("zinc", "substance:10")])
    rule_doses(c)
    rule_counterfactual_article(c)
    assert "R-DOSE-OVERMAX-HIDDEN" in codes(c)
    assert c.facts["counterfactual_article"] == "ART_18"


def test_equivalence_rows_are_not_doses():
    decl = declaration([item("plant", "plant:1", "Curcuma longa L.", 500)])
    lab = label([ingredient("Curcuma")], [comp_row("Équivalent plante : 2 g", "Curcuma", 2, "g")])
    c = ctx_for(decl, lab, [resolution("Curcuma", "plant:1"), resolution("Curcuma", "plant:1")])
    rule_doses(c)
    assert not [f for f in c.findings if f.code.startswith("R-DOSE")]


def test_massive_undeclared_is_blocking():
    decl = declaration([item("plant", "plant:1", "Curcuma longa L.", 300)])
    names = ["curcuma", "HPMC", "thé vert", "Ephedra sinica", "zinc gluconate"]
    uids = ["plant:1", "ingredient:20", "plant:3", "plant:2", "ingredient:21"]
    lab = label([ingredient(n) for n in names])
    c = ctx_for(decl, lab, [resolution(n, u) for n, u in zip(names, uids)])
    rule_completeness(c)
    assert "R-ING-MASSIVE" in codes(c)


def test_mention_absent_by_model_but_present_in_text_is_not_flagged():
    lab = label(
        [ingredient("curcuma")],
        ments=mentions(warning_do_not_exceed=mention("absent")),
        text="Curcuma. Ne pas dépasser la dose journalière recommandée. Produit Test",
    )
    c = ctx_for(declaration([item("plant", "plant:1", "Curcuma longa L.")]), lab, [resolution("curcuma", "plant:1")])
    rule_mentions(c)
    assert "R-MEN-warning_do_not_exceed" not in codes(c)


def test_three_core_mentions_missing_is_fake_label():
    m = mentions(
        warning_do_not_exceed=mention("absent"),
        warning_varied_diet=mention("absent"),
        warning_children=mention("absent"),
    )
    lab = label([ingredient("curcuma")], ments=m, text="Curcuma. Produit Test. 2 gélules par jour")
    c = ctx_for(declaration([item("plant", "plant:1", "Curcuma longa L.")]), lab, [resolution("curcuma", "plant:1")])
    rule_mentions(c)
    assert "R-MEN-FAKE" in codes(c)


def test_ocr_image_links_are_not_placeholders():
    lab = label([ingredient("curcuma")], text="![img-0.jpeg](img-0.jpeg) Curcuma Produit Test Lot : XXX")
    c = ctx_for(declaration([item("plant", "plant:1", "Curcuma longa L.")]), lab, [resolution("curcuma", "plant:1")])
    rule_document(c)
    assert "R-DOC-PLACEHOLDER" not in codes(c)


def test_not_a_label_document():
    lab = label([ingredient("curcuma")], kind=DocumentKind.form_screenshot)
    c = ctx_for(declaration([item("plant", "plant:1", "Curcuma longa L.")]), lab, [resolution("curcuma", "plant:1")])
    rule_document(c)
    assert "R-DOC-NOT-LABEL" in codes(c)


def _finding(sev, conf, grounded=True, verified=None):
    return Finding(
        id="F1",
        code="X",
        severity=sev,
        fraud_type=FraudType.fake_label,
        confidence=conf,
        title="t",
        detail="d",
        grounded=grounded,
        verified=verified,
    )


def test_decision_requires_proof_and_respects_refutation():
    assert decide([_finding(Severity.BLOCKING, 0.9)], S, "p", {}).decision == "BLOCK"
    assert decide([_finding(Severity.BLOCKING, 0.9, grounded=False)], S, "p", {}).decision == "PASS"
    assert (
        decide([_finding(Severity.BLOCKING, 0.9, grounded=False, verified="confirmed")], S, "p", {}).decision
        == "BLOCK"
    )
    assert decide([_finding(Severity.BLOCKING, 0.99, verified="refuted")], S, "p", {}).decision == "PASS"
    assert decide([_finding(Severity.BLOCKING, 0.6)], S, "p", {}).decision == "PASS"
    assert risk_score([_finding(Severity.MINOR, 0.9)]) < 0.1
