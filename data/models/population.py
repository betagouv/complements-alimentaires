from django.db import models

from .abstract_models import CommonBaseModel


class Population(CommonBaseModel):
    class Meta:
        verbose_name = "Population cible / à risque"

    min_age = models.FloatField(blank=True, null=True, default=None)
    max_age = models.FloatField(blank=True, null=True, default=None)
    siccrf_id = models.IntegerField(blank=True, null=True, editable=False, db_index=True, unique=True)
    is_defined_by_anses = models.BooleanField(default=False)


class Condition(CommonBaseModel):
    class Meta:
        verbose_name = "condition de santé / facteurs de risque"

    name_en = models.TextField(blank=True)
