"""Offline tests of ai_v2 (no network, no database): `python -m pytest ai_v2/tests`.

They are written for pytest and need the packages of ai_v2/requirements.txt, which the Django app
does not install. `load_tests` below stops Django's test runner (`manage.py test`, run by the CI)
from importing them, so the app's CI is not affected by this package.
"""


def load_tests(loader, standard_tests, pattern):
    # unittest discovery protocol: returning the (empty) suite as is means "nothing to load here".
    return standard_tests
