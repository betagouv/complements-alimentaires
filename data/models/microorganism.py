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


class Microorganism(CommonModel, WithSICCRFComments, WithCAComments):
    class Meta:
        verbose_name = "micro-organisme"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_genre = models.TextField(verbose_name="genre de micro-organisme (selon la base SICCRF)")
    CA_genre = models.TextField(verbose_name="genre de micro-organisme")
    substances = models.ManyToManyField(Substance, through="MicroorganismSubstanceRelation")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete", "genre"])
    genre = models.GeneratedField(
        expression=Coalesce(F("CA_genre"), F("siccrf_genre")),
        output_field=models.TextField(verbose_name="genre de micro-organisme"),
        db_persist=True,
    )

    @property
    def name_en(self):
        return self.siccrf_name_en


class MicroorganismSubstanceRelation(WithCreationAndModificationDate, WithHistory):
    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée au micro-organisme (selon la base SICCRF)"
    )
    CA_is_related = models.BooleanField(default=False, verbose_name="substance associée au micro-organisme")


class MicroorganismSynonym(WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean):
    class Meta:
        verbose_name = "synonyme de micro-organisme"

    standard_name = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    name = models.TextField(verbose_name="nom")
    siccrf_is_obsolete = models.BooleanField(verbose_name="objet obsolète selon SICCRF", default=False)
