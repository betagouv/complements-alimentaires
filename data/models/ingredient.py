from django.db import models

from simple_history.models import HistoricalRecords

from data.behaviours import Historisable, TimeStampable

from .abstract_ingredient_models import IngredientCommonModel
from .abstract_ingredient_relation_models import (
    MaxQuantityPerPopulationRelationCommonModel,
    SynonymCommonModel,
)
from .ingredient_type import IngredientType
from .mixins import PublicReasonHistoricalModel
from .population import Population
from .substance import Substance
from .unit import Unit


class Ingredient(IngredientCommonModel):
    class Meta:
        verbose_name = "autre ingrédient"
        verbose_name_plural = "autres ingrédients"

    ingredient_type = models.IntegerField(
        choices=IngredientType.choices,
        null=True,
        verbose_name="type de l'ingrédient",
    )
    substances = models.ManyToManyField(Substance, through="IngredientSubstanceRelation")
    max_quantities = models.ManyToManyField(Population, through="IngredientMaxQuantityPerPopulationRelation")
    unit = models.ForeignKey(
        Unit,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="unité des quantités spécifiées (quantité max, apport de référence)",
    )

    history = HistoricalRecords(
        bases=[
            PublicReasonHistoricalModel,
        ],
        inherit=True,
    )

    @property
    def object_type(self):
        """
        overwrites object_type property from CommonModel
        """
        if self.ingredient_type:
            return IngredientType(self.ingredient_type).name.lower()
        else:
            return self.__class__.__name__.lower()


class IngredientSubstanceRelation(TimeStampable, Historisable):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)


class IngredientSynonym(SynonymCommonModel):
    class Meta:
        verbose_name = "synonyme d'ingrédient"
        constraints = [
            models.UniqueConstraint(
                fields=["standard_name", "name"],
                name="unicity_ingredient_synonym",
            )
        ]

    standard_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class IngredientMaxQuantityPerPopulationRelation(MaxQuantityPerPopulationRelationCommonModel):
    class Meta:
        verbose_name = "quantité maximum de ingredient autorisée pour une population cible"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "population"],
                name="unique_ingredient_max_quantity_per_population",
            )
        ]

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
