from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.db.models.base import ModelBase

FIXTURE_FOLDER = settings.BASE_DIR / "fixtures"


def get_models() -> list[ModelBase]:
    """Return all installed models using introspection, except the backlisted one
    because they are useless and can create integrity errors during deserialization.
    """
    model_data = [
        # Useful Django models
        ("auth", "Permission"),
        ("auth", "Group"),
        # Our models (order matters because of model relations)
        ("data", "User"),
        ("data", "Company"),
        ("data", "CompanySupervisor"),
        ("data", "Declarant"),
        ("data", "BlogPost"),
        ("data", "Webinar"),
    ]
    return [apps.get_model(d[0], d[1]) for d in model_data]


def get_full_path(model: ModelBase) -> Path:
    return FIXTURE_FOLDER / f"{get_model_path(model)}.yaml"


def get_model_path(model: ModelBase) -> str:
    return f"{model._meta.app_label}.{model._meta.object_name}"
