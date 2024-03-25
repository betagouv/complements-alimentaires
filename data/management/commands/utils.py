from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.db.models.base import ModelBase

FIXTURE_FOLDER = settings.BASE_DIR / "data" / "fixtures"


def get_models() -> list[ModelBase]:
    """Return all installed models using introspection, except the backlisted one
    because they are useless and can create integrity errors during deserialization.
    """
    BLACKLISTED_APPS = ["sessions", "admin"]
    return [model for model in apps.get_models() if model._meta.app_label not in BLACKLISTED_APPS]


def get_full_path(model: ModelBase) -> Path:
    return FIXTURE_FOLDER / f"{get_model_path(model)}.yaml"


def get_model_path(model: ModelBase) -> str:
    return f"{model._meta.app_label}.{model._meta.object_name}"
