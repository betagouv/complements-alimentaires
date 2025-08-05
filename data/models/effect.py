from django.db import models
from simple_history.models import HistoricalRecords

from .abstract_models import CommonModel


class Effect(CommonModel):
    class Meta:
        verbose_name = "Objectif et effet des compléments alimentaires"
        verbose_name_plural = "Objectifs et effets des compléments alimentaires"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais selon la base SICCRF")
    history = HistoricalRecords(inherit=True)

    @property
    def name_en(self):
        return self.siccrf_name_en
