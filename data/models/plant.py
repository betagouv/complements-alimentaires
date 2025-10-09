from django.db import models

from simple_history.models import HistoricalRecords

from data.behaviours import Historisable, TimeStampable

from .abstract_ingredient_models import CommonModel, IngredientCommonModel
from .abstract_ingredient_relation_models import (
    MaxQuantityPerPopulationRelationCommonModel,
    SynonymCommonModel,
)
from .mixins import PublicReasonHistoricalModel
from .population import Population
from .substance import Substance
from .unit import Unit


class PlantFamily(CommonModel):
    class Meta:
        verbose_name = "famille de plantes"
        verbose_name_plural = "familles de plantes"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    history = HistoricalRecords(inherit=True)

    @property
    def name_en(self):
        return self.siccrf_name_en


class PlantPart(CommonModel):
    class Meta:
        verbose_name = "partie de plante"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    history = HistoricalRecords(
        inherit=True,
    )

    @property
    def name_en(self):
        return self.siccrf_name_en


class Plant(IngredientCommonModel):
    class Meta:
        verbose_name = "plante"

    family = models.ForeignKey(
        PlantFamily, on_delete=models.SET_NULL, null=True, verbose_name="famille de plante", related_name="plant_set"
    )

    plant_parts = models.ManyToManyField(PlantPart, through="Part", verbose_name="partie de plante")
    substances = models.ManyToManyField(Substance, through="PlantSubstanceRelation")
    max_quantities = models.ManyToManyField(Population, through="PlantMaxQuantityPerPopulationRelation")
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


class Part(TimeStampable):
    """
    Ce modèle permet d'associer des données supplémentaires à la relation ManyToMany
    plant_parts
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    plantpart = models.ForeignKey(PlantPart, on_delete=models.CASCADE)

    must_be_monitored = models.BooleanField(default=False, verbose_name="⚠️ à surveiller ?")

    is_useful = models.BooleanField(default=False, verbose_name="🍵 utile ?")
    history = HistoricalRecords(inherit=True)


class PlantSubstanceRelation(TimeStampable, Historisable):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)


class PlantSynonym(SynonymCommonModel):
    class Meta:
        verbose_name = "synonyme de plante"
        constraints = [
            models.UniqueConstraint(
                fields=["standard_name", "name"],
                name="unicity_plant_synonym",
            )
        ]

    standard_name = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")


class PlantMaxQuantityPerPopulationRelation(MaxQuantityPerPopulationRelationCommonModel):
    class Meta:
        verbose_name = "quantité maximum de plant autorisée pour une population cible"
        constraints = [
            models.UniqueConstraint(
                fields=["plant", "population"],
                name="unique_plant_max_quantity_per_population",
            )
        ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
