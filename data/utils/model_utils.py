from typing import Iterable
from django.apps import apps
from django.db.models.base import ModelBase


def get_models(model_data: Iterable[tuple[str, str]]) -> list[ModelBase]:
    """Return actual models from an iterable of model data"""
    return [apps.get_model(md[0], md[1]) for md in model_data]
