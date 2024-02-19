from django.db import models

from .abstract_models import CommonModel


class Condition(CommonModel):
    class Meta:
        verbose_name = "condition de santé / facteurs de risque"

    siccrf_name_en = models.TextField(blank=True)
