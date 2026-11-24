"""Units, quote grounding, strict schemas, cache, safe calculator and metrics."""

import pytest

from ai_v2.agent import safe_calc
from ai_v2.cache import Cache
from ai_v2.eval.gold_v1 import GoldEntry
from ai_v2.eval.metrics import evaluate
from ai_v2.llm import strict_schema
from ai_v2.schemas import LabelExtraction
from ai_v2.text import e_numbers, quote_in_text
from ai_v2.units import convert


def test_units():
    assert convert(1, "mg", "µg") == 1000
    assert convert(500, "µg", "mg") == 0.5
    assert convert(1000, "UI", "µg", "vitamine D3") == 25
    assert convert(10, "milliards UFC", "UFC") == 1e10
    assert convert(5, "ml", "g") is None


def test_quote_grounding_tolerates_ocr_noise():
    text = "INGREDIENTS : Extrait sec de racine de Rhodiola rosea (3% rosavines), gelule vegetale (HPMC)."
    assert quote_in_text("Extrait sec de racine de Rhodiola rosea", text) == 100
    assert quote_in_text("Extrait sec de racine de Rhodiola rossea", text) >= 85
    assert quote_in_text("Ginkgo biloba", text) < 70
    assert e_numbers("acide citrique (E 330), E160a") == ["E330", "E160a"]


def test_strict_schema_is_self_contained():
    sch = strict_schema(LabelExtraction)
    raw = str(sch)
    assert "$ref" not in raw and "$defs" not in raw

    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "object" and "properties" in n:
                assert n["additionalProperties"] is False
                assert set(n["required"]) == set(n["properties"])
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(sch)


def test_cache_roundtrip(tmp_path):
    c = Cache(tmp_path / "c.sqlite")
    k = c.key("extract", file="abc", prompt="p1")
    assert k == c.key("extract", prompt="p1", file="abc")  # key order does not matter
    assert c.get(k) is None
    c.set(k, {"a": 1})
    assert c.get(k) == {"a": 1}
    assert c.key("extract", file="abc", prompt="p2") != k  # changing the prompt invalidates the cache


def test_safe_calc_is_sandboxed():
    assert safe_calc("500*0.95*2") == 950
    with pytest.raises(ValueError):
        safe_calc("__import__('os').system('dir')")


def test_metrics_count_true_positives():
    # regression test for the bug of the legacy ai/scripts/testing.py: a correctly blocked fraud MUST count as a TP
    gold = [
        GoldEntry(key="a", split="positive", snapshot_id=1, declaration_id=1, expected_block=True),
        GoldEntry(key="b", split="negative", snapshot_id=2, declaration_id=2, expected_block=False),
    ]
    res = {
        "a": {"decision": {"decision": "BLOCK", "risk_score": 0.99, "reason_codes": ["R-ART-BYPASS"]}, "findings": []},
        "b": {"decision": {"decision": "PASS", "risk_score": 0.1, "reason_codes": []}, "findings": []},
    }
    m = evaluate(gold, res)["end_to_end"]
    assert (m["tp"], m["fp"], m["fn"], m["tn"]) == (1, 0, 0, 1)
    assert m["precision"] == 1.0 and m["recall"] == 1.0
