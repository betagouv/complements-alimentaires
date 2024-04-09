from django.db import models
from simple_history.models import HistoricalRecords

from .abstract_models import CommonModel


class GalenicFormulation(CommonModel):
    class Meta:
        verbose_name = "Forme galénique"
        verbose_name_plural = "Formes galéniques"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais selon la base SICCRF")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete"])

    @property
    def name_en(self):
        return self.siccrf_name_en
