from django.db import models

from .abstract_models import SICCRFCommonModel


class Condition(SICCRFCommonModel):
    class Meta:
        verbose_name = "condition de santé / facteurs de risque"

    siccrf_name_en = models.TextField(blank=True)
