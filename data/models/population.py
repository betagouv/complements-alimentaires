from django.db import models

from .abstract_models import CommonBaseModel


class Population(CommonBaseModel):
    class Meta:
        verbose_name = "Population cible / à risque"

    name_en = models.TextField(blank=True)


class Condition(CommonBaseModel):
    class Meta:
        verbose_name = "condition de santé / facteurs de risque"

    name_en = models.TextField(blank=True)
