from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import F

from simple_history.models import HistoricalRecords

from .mixins import (
    WithCreationAndModificationDate,
    WithHistory,
    WithMissingImportBoolean,
    WithSICCRFComments,
    WithCAComments,
)
from .abstract_models import CommonModel
from .substance import Substance


class PlantFamily(CommonModel):
    class Meta:
        verbose_name = "famille de plantes"
        verbose_name_plural = "familles de plantes"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete"])

    @property
    def name_en(self):
        return self.siccrf_name_en


class PlantPart(CommonModel):
    class Meta:
        verbose_name = "partie de plante"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete"])

    @property
    def name_en(self):
        return self.siccrf_name_en


class Plant(CommonModel, WithSICCRFComments, WithCAComments):
    class Meta:
        verbose_name = "plante"

    siccrf_family = models.ForeignKey(
        PlantFamily,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="famille de plante (selon la base SICCRF)",
        related_name="siccrf_plant_set",
    )
    ca_family = models.ForeignKey(
        PlantFamily,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="famille de plante",
        related_name="ca_plant_set",
    )
    # TODO: output_field should be a ForeignKey
    family = models.GeneratedField(
        expression=Coalesce(F("ca_family"), F("siccrf_family")),
        output_field=models.BigIntegerField(verbose_name="famille de plante"),
        db_persist=True,
    )
    plant_parts = models.ManyToManyField(PlantPart, through="Part", verbose_name="partie de plante")
    substances = models.ManyToManyField(Substance, through="PlantSubstanceRelation")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete", "family"])


class Part(WithCreationAndModificationDate):
    """
    Ce modèle permet d'associer des données supplémentaires à la relation ManyToMany
    plant_parts
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    plantpart = models.ForeignKey(PlantPart, on_delete=models.CASCADE)
    siccrf_must_be_monitored = models.BooleanField(
        default=False, verbose_name="⚠️ à surveiller (selon la base SICCRF) ?"
    )
    ca_must_be_monitored = models.BooleanField(null=True, default=None, verbose_name="⚠️ à surveiller ?")
    must_be_monitored = models.GeneratedField(
        expression=Coalesce(F("ca_must_be_monitored"), F("siccrf_must_be_monitored")),
        output_field=models.BooleanField(verbose_name="⚠️ à surveiller ?"),
        db_persist=True,
    )
    siccrf_is_useful = models.BooleanField(default=False, verbose_name="🍵 utile (selon la base SICCRF) ?")
    ca_is_useful = models.BooleanField(null=True, default=None, verbose_name="🍵 utile ?")
    is_useful = models.GeneratedField(
        expression=Coalesce(F("ca_is_useful"), F("siccrf_is_useful")),
        output_field=models.BooleanField(verbose_name="🍵 utile ?"),
        db_persist=True,
    )
    history = HistoricalRecords(
        inherit=True, excluded_fields=["name", "is_obsolete", "must_be_monitored", "is_useful"]
    )


class PlantSubstanceRelation(WithCreationAndModificationDate, WithHistory):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée à la plante (selon la base SICCRF)"
    )
    ca_is_related = models.BooleanField(null=True, default=None, verbose_name="substance associée à la plante")


class PlantSynonym(WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean):
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
