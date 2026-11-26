"""Decision policy and the "be sure before blocking" guardrails, each motivated by a real false
positive seen during the test runs (product names below are made up)."""

from types import SimpleNamespace

from ai_v2.config import Settings
from ai_v2.decision import decide
from ai_v2.label_index import LabelIndex
from ai_v2.schemas import Finding, FraudType, Severity


def _f(code, sev, conf, verified=None, i=1):
    return Finding(
        id=f"F{i}",
        code=code,
        severity=sev,
        fraud_type=FraudType.label_noncompliance,
        confidence=conf,
        title="t",
        detail="d",
        verified=verified,
    )


def test_uncertain_findings_never_block():
    # real case: French statements printed upside down, the agent answers "uncertain" -> no block
    s = Settings()
    fs = [_f(f"R-MEN-{k}", Severity.MAJOR, 0.85, "uncertain", i) for i, k in enumerate("abcdef")]
    fs.append(_f("R-MEN-FAKE", Severity.BLOCKING, 0.95, "uncertain", 9))
    assert decide(fs, s, "p", {}).decision == "PASS"


def test_confirmed_major_blocks_only_if_in_policy():
    s = Settings()
    f = [_f("R-MEN-warning_children", Severity.MAJOR, 0.95, "confirmed")]
    assert decide(f, s, "p", {}).decision == "PASS"  # "mentions" are not in the default policy
    s.confirmed_major_codes = ("R-MEN-",)
    assert decide(f, s, "p", {}).decision == "BLOCK"


def test_nrv_consistency_catches_misread_nutrient():
    from ai_v2.rules import nrv_consistent

    # real case: "Magnésium 56,26 mg (15 % AR)" read as "Manganèse 56,25 mg (150 %)"
    assert nrv_consistent("manganèse", 56.25, "mg", 150) is False
    assert nrv_consistent("magnésium", 56.25, "mg", 15) is True
    assert nrv_consistent("vitamine D3", 5, "µg", 100) is True
    assert nrv_consistent("curcumine", 95, "mg", 10) is None


def test_agent_confirmation_must_be_supported():
    from ai_v2.agent import VerificationAgent
    from ai_v2.extract import MergedLabel

    from .factories import refdata

    agent = object.__new__(VerificationAgent)  # no client needed for _confirmation_supported
    agent.ref = refdata()
    label = MergedLabel(files=[], extra_text="Magnésium / Magnesium 56.26 mg (15% AR). Zinc 10 mg.")
    f = Finding(
        id="F1",
        code="R-DOSE-OVERMAX-HIDDEN",
        severity=Severity.BLOCKING,
        fraud_type=FraudType.dose_underdeclared,
        confidence=0.9,
        title="t",
        detail="d",
        refs=["substance:10"],
    )  # zinc
    assert agent._confirmation_supported(f, "Zinc 10 mg", label, looked=True)[0]
    assert not agent._confirmation_supported(f, "Magnésium / Magnesium 56.26 mg", label, looked=True)[
        0
    ]  # another element
    assert not agent._confirmation_supported(f, "Zinc 25 mg par gélule", label, looked=True)[0]  # made-up quote
    m = Finding(
        id="F2",
        code="R-MEN-warning_children",
        severity=Severity.MAJOR,
        fraud_type=FraudType.label_noncompliance,
        confidence=0.9,
        title="t",
        detail="d",
    )
    assert not agent._confirmation_supported(m, None, label, looked=False)[0]
    assert agent._confirmation_supported(m, None, label, looked=True)[0]


def test_warning_keywords_double_check():
    from ai_v2.rules import warning_keywords_present

    # real case: the warnings were present, but condensed in very small print
    label = (
        "Déconseillé aux personnes diabétiques ou pré-diabétiques, asthmatiques, traitées par anti-vitamine K "
        "ou sous traitements anticoagulants. Déconseillé chez les personnes présentant une allergie alimentaire "
        "aux crustacés et aux insectes ou dont l'alimentation est contrôlée pour le sodium, le potassium ou le calcium."
    )
    assert warning_keywords_present(
        "Déconseillé aux personnes présentant une allergie alimentaire aux crustacés ou aux insectes.", label
    )
    assert warning_keywords_present(
        "Déconseillé aux personnes diabétiques ou pré-diabétiques, asthmatiques ou traitées par " "anti-vitamine K.",
        label,
    )
    assert not warning_keywords_present(
        "L'emploi chez les femmes enceintes est déconseillé.", "Ne pas dépasser la dose."
    )


def test_label_reuse_across_different_products(tmp_path):
    idx = LabelIndex(tmp_path / "idx.json")
    page = SimpleNamespace(dhash="323696b2b2daa8b0")
    doc = SimpleNamespace(pages=[page])
    a = SimpleNamespace(declaration_id=1, name="Vitamin B Complex", company_id=7)
    b = SimpleNamespace(declaration_id=2, name="Turmeric Capsules", company_id=7)
    c = SimpleNamespace(declaration_id=3, name="Vitamin B Complex Forte", company_id=7)
    txt = "COLLAGEN CAPSULES BRANDX Hydrolyzed Collagen, Pectin, Citric Acid, Natural Strawberry Flavor"
    assert idx.check_and_add(a, [doc], txt) == []
    near = SimpleNamespace(pages=[SimpleNamespace(dhash="323696b2b2daa8b1")])  # 1 bit apart
    assert [e["declaration_id"] for e in idx.check_and_add(b, [near], txt)] == [1]
    assert all(
        e["name"] != "Vitamin B Complex" for e in idx.check_and_add(c, [doc], txt)
    )  # same product declared again
    # same graphic template within a product range, different content (real case: bud macerates): nothing
    d = SimpleNamespace(declaration_id=4, name="Angélique", company_id=8)
    assert idx.check_and_add(d, [doc], "Macérat de bourgeons Angelica sylvestris glycérine alcool") == []
