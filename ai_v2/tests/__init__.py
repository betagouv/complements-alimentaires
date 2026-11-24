"""Offline tests of ai_v2 (no network, no database): `python -m pytest ai_v2/tests`.

They need the packages of ai_v2/requirements.txt, which the Django app does not install; the
`load_tests` hook in ai_v2/__init__.py keeps them out of `manage.py test`.
"""
