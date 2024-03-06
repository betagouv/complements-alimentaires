from django.db import models
from simple_history.models import HistoricalRecords

from .abstract_models import CommonModel


class Condition(CommonModel):
    class Meta:
        verbose_name = "condition de santé / facteurs de risque"

    siccrf_name_en = models.TextField(blank=True)
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete"])

    @property
    def name_en(self):
        return self.siccrf_name_en
