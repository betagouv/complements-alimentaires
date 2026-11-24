"""Compl'Alim: label-fraud detection pipeline, v2.

Principle: the AI reads and matches, the code judges, an agent double-checks the doubtful cases,
and the decision (BLOCK / PASS) is automatic and backed by evidence.

The package is standalone (no Django dependency), so that it can run locally against the
production database in read-only mode; see README.md for the integration plan in the app.
"""

__version__ = "2.0.0"
