from django.db import models

from .abstract_models import SICCRFCommonModel


class Population(SICCRFCommonModel):
    class Meta:
        verbose_name = "Population cible / à risque"

    min_age = models.FloatField(blank=True, null=True, default=None)
    max_age = models.FloatField(blank=True, null=True, default=None)
    is_defined_by_anses = models.BooleanField(default=False)
