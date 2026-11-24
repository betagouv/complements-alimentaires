"""Pure article calculation (article.compute_article), one test per branch of the app's logic."""

from ai_v2.article import (
    ANSES_REFERAL,
    ART_15,
    ART_15_HIGH_RISK_POPULATION,
    ART_15_WARNING,
    ART_16,
    ART_18,
    CompItem,
    CompSubstance,
    Composition,
    compute_article,
)

from .factories import ENCEINTES, refdata

REF = refdata()


def comp(items=(), subs=(), pops=(), galenic=1, siccrf=None):
    return Composition(
        declaration_id=1,
        items=list(items),
        computed_substances=list(subs),
        populations=list(pops),
        galenic_formulation_id=galenic,
        siccrf_id=siccrf,
    )


def test_art15_simple():
    assert compute_article(comp([CompItem("plant", "plant:1")]), REF).article == ART_15


def test_empty_and_historical():
    assert compute_article(comp(), REF).article == ""
    assert compute_article(comp([CompItem("plant", "plant:1")], siccrf=12), REF).article is None


def test_unauthorized_plant_is_art16():
    assert compute_article(comp([CompItem("plant", "plant:1"), CompItem("plant", "plant:2")]), REF).article == ART_16


def test_new_ingredient_is_art16_unless_replaced():
    assert compute_article(comp([CompItem("ingredient", None, new=True)]), REF).article == ART_16
    assert (
        compute_article(
            comp([CompItem("plant", "plant:1"), CompItem("ingredient", None, new=True, request_status="REPLACED")]),
            REF,
        ).article
        == ART_15
    )


def test_nutrient_overdose_is_art18_and_other_is_anses():
    assert compute_article(comp(subs=[CompSubstance("substance:10", 25.0)]), REF).article == ART_18
    assert compute_article(comp(subs=[CompSubstance("substance:11", 2.0)]), REF).article == ANSES_REFERAL
    assert (
        compute_article(comp(subs=[CompSubstance("substance:11", 1.9)]), REF).article == ART_15
    )  # equal to the max: OK


def test_population_specific_max():
    # caffeine: 200 mg for the general population, 0 for pregnant women
    assert (
        compute_article(comp(subs=[CompSubstance("substance:12", 50.0)], pops=[ENCEINTES]), REF).article
        == ANSES_REFERAL
    )


def test_risky_plant_had_regex_alcohol_and_galenic():
    assert compute_article(comp([CompItem("plant", "plant:3")]), REF).article == ART_15_WARNING
    assert compute_article(comp([CompItem("plant", "plant:4")]), REF).article == ART_15_WARNING
    assert compute_article(comp([CompItem("plant", "plant:1", preparation_id=5)]), REF).article == ART_15_WARNING
    assert compute_article(comp([CompItem("plant", "plant:1")], galenic=9), REF).article == ART_15_WARNING


def test_high_risk_population():
    assert (
        compute_article(comp([CompItem("plant", "plant:1")], pops=[ENCEINTES]), REF).article
        == ART_15_HIGH_RISK_POPULATION
    )
