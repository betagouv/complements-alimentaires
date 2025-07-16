from django.db import models

from simple_history.models import HistoricalRecords

from data.behaviours import Historisable, TimeStampable

from .abstract_models import CommonModel, IngredientCommonModel
from .mixins import PublicReasonHistoricalModel
from .substance import Substance


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

    # TODO: ce champ n'est pas utile en tant que tel, il serait possible de l'éviter en créant un Field custom ForeignGeneratedField(ForeigObject)
    family_by_id = models.BigIntegerField(verbose_name="famille de plante", null=True)
    family = models.ForeignObject(
        PlantFamily,
        on_delete=models.SET_NULL,
        from_fields=["family_by_id"],
        to_fields=["id"],
        related_name="plant_set",
        null=True,
    )

    plant_parts = models.ManyToManyField(PlantPart, through="Part", verbose_name="partie de plante")
    substances = models.ManyToManyField(Substance, through="PlantSubstanceRelation")
    history = HistoricalRecords(
        bases=[
            PublicReasonHistoricalModel,
        ],
        inherit=True,
        excluded_fields=[
            "family",
        ],
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


class PlantSynonym(TimeStampable, Historisable):
    class Meta:
        verbose_name = "synonyme de plante"

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    standard_name = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")
    name = models.TextField(verbose_name="nom")
    siccrf_is_obsolete = models.BooleanField(verbose_name="objet obsolète selon SICCRF", default=False)
    # TODO importer aussi les synonym_type = TYSYN_IDENT en ForeignKeys

    @property
    def is_obsolete(self):
        return self.siccrf_is_obsolete

    def __str__(self):
        return self.name
