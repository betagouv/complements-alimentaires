from django.db import models

from simple_history.models import HistoricalRecords

from .abstract_ingredient_models import CommonModel
from .mixins import WithIsRiskyBoolean


class GalenicFormulation(CommonModel, WithIsRiskyBoolean):
    class Meta:
        verbose_name = "forme galénique"
        verbose_name_plural = "formes galéniques"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais selon la base SICCRF")
    is_liquid = models.BooleanField(default=False, verbose_name="la forme galénique est-elle une forme liquide ?")
    history = HistoricalRecords(inherit=True)

    @property
    def name_en(self):
        return self.siccrf_name_en
