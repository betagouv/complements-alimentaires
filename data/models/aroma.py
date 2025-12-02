from django.db import models

from data.models.abstract_ingredient_models import CommonModel
from data.models.ingredient_status import IngredientStatus, WithStatus

from .abstract_ingredient_relation_models import (
    SynonymCommonModel,
)


class Aroma(CommonModel, WithStatus):
    class Meta:
        verbose_name = "arôme"

    status = IngredientStatus.NO_STATUS
    description = models.TextField(blank=True)


class AromaSynonym(SynonymCommonModel):
    class Meta:
        verbose_name = "synonyme d'arome"
        constraints = [
            models.UniqueConstraint(
                fields=["standard_name", "name"],
                name="unicity_aroma_synonym",
            )
        ]

    standard_name = models.ForeignKey(Aroma, on_delete=models.CASCADE, verbose_name="nom de référence")
