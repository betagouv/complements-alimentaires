from django.db import models

from simple_history.models import HistoricalRecords

from data.behaviours import Historisable, TimeStampable

from .abstract_models import IngredientCommonModel, SynonymType
from .ingredient_type import IngredientType
from .mixins import PublicReasonHistoricalModel
from .substance import Substance


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


class IngredientSynonym(TimeStampable, Historisable):
    class Meta:
        verbose_name = "synonyme d'ingrédient"
        constraints = [
            models.UniqueConstraint(
                fields=["standard_name", "name"],
                name="unicity_ingredient_synonym",
            )
        ]

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    standard_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    name = models.TextField(verbose_name="nom")
    synonym_type = models.CharField(
        choices=SynonymType.choices, default=SynonymType.FRENCH, verbose_name="type de synonyme"
    )

    def __str__(self):
        return self.name
