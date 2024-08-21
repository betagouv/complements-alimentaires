from django.db import models
from simple_history.models import HistoricalRecords

from .abstract_models import CommonModel


class Population(CommonModel):
    class Meta:
        verbose_name = "Population cible"
        verbose_name_plural = "Populations cibles"

    min_age = models.FloatField(blank=True, null=True, default=None)
    max_age = models.FloatField(blank=True, null=True, default=None)
    is_defined_by_anses = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete"])
