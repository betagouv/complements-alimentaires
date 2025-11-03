from django.db import models
from django.db.models import F, Value

from simple_history.models import HistoricalRecords

from data.behaviours import Historisable, TimeStampable

from .abstract_ingredient_models import IngredientCommonModel
from .abstract_ingredient_relation_models import (
    MaxQuantityPerPopulationRelationCommonModel,
    SynonymCommonModel,
)
from .mixins import PublicReasonHistoricalModel
from .population import Population
from .substance import Substance


# cette fonction remplace le fonction Concat qui est mutable avec PSQL
# les GeneratedFields doivent avoir des expression de génération immutables
# Avec Django 5.1 ce problème sera résolu https://forum.djangoproject.com/t/using-generatedfield-with-postgres/27224/4
class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"


class Microorganism(IngredientCommonModel):
    class Meta:
        verbose_name = "micro-organisme"

    name = models.GeneratedField(
        expression=ConcatOp(
            F("genus"),
            Value(" "),
            F("species"),
        ),
        output_field=models.TextField(verbose_name="nom"),
        db_persist=True,
    )

    genus = models.TextField(verbose_name="genre de micro-organisme", null=True)

    species = models.TextField(verbose_name="espèce de micro-organisme", null=True)

    substances = models.ManyToManyField(Substance, through="MicroorganismSubstanceRelation")
    max_quantities = models.ManyToManyField(Population, through="MicroorganismMaxQuantityPerPopulationRelation")

    history = HistoricalRecords(
        bases=[
            PublicReasonHistoricalModel,
        ],
        inherit=True,
        excluded_fields=[
            "name",
        ],
    )


class MicroorganismSubstanceRelation(TimeStampable, Historisable):
    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)


class MicroorganismSynonym(SynonymCommonModel):
    class Meta:
        verbose_name = "synonyme de micro-organisme"
        constraints = [
            models.UniqueConstraint(
                fields=["standard_name", "name"],
                name="unicity_microorganism_synonym",
            )
        ]

    standard_name = models.ForeignKey(Microorganism, on_delete=models.CASCADE)


class MicroorganismMaxQuantityPerPopulationRelation(MaxQuantityPerPopulationRelationCommonModel):
    class Meta:
        verbose_name = "quantité maximum de microorganism autorisée pour une population cible"
        constraints = [
            models.UniqueConstraint(
                fields=["microorganism", "population"],
                name="unique_microorganism_max_quantity_per_population",
            )
        ]

    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
