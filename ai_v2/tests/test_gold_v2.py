"""Import of the hand-annotated dataset (eval/gold_v2.py)."""

from ai_v2.eval.gold_v2 import import_gold_v2


def test_import_csv_semicolon(tmp_path):
    p = tmp_path / "annot.csv"
    p.write_text(
        "declaration_id;expected_block;fraud_types;notes\n"
        "123;oui;undeclared_ingredients|dose_underdeclared;thé vert non déclaré\n"
        "456;non;;\n",
        encoding="utf-8",
    )
    g = import_gold_v2(p)
    assert [e.key for e in g] == ["decl:123", "decl:456"]
    assert g[0].expected_block is True and g[1].expected_block is False
    assert {i.category.value for i in g[0].structured.issues} == {"undeclared_ingredient", "dose_inconsistency"}
