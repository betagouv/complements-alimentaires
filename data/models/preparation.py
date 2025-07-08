from django.db import models

from simple_history.models import HistoricalRecords

from .abstract_models import CommonModel


class Preparation(CommonModel):
    class Meta:
        verbose_name = "préparation de plantes"
        verbose_name_plural = "préparations de plantes"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais selon la base SICCRF")
    contains_alcohol = models.BooleanField(default=False, verbose_name="la préparation contient-elle de l'alcool ?")
    history = HistoricalRecords(inherit=True)

    @property
    def name_en(self):
        return self.siccrf_name_en
