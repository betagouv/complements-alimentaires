"""Compl'Alim: label-fraud detection pipeline, v2.

Principle: the AI reads and matches, the code judges, an agent double-checks the doubtful cases,
and the decision (BLOCK / PASS) is automatic and backed by evidence.

The package is standalone (no Django dependency), so that it can run locally against the
production database in read-only mode; see README.md for the integration plan in the app.
"""

__version__ = "2.0.0"


def load_tests(loader, standard_tests, pattern):
    """Keep this whole package out of Django's test runner (`manage.py test`, run by the CI).

    Its modules need packages the app does not install (httpx, pydantic, rapidfuzz...), so letting
    unittest discovery import them would fail. The package's own tests are pytest tests, run with
    `python -m pytest ai_v2/tests`. Returning the (empty) suite as is tells unittest not to look inside.
    """
    return standard_tests
