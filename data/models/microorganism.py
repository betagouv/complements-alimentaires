from django.db import models
from django.db.models.functions import Coalesce, NullIf
from django.db.models import F, Value

from simple_history.models import HistoricalRecords

from data.behaviours import TimeStampable, Historisable
from .mixins import WithMissingImportBoolean, WithComments
from .abstract_models import CommonModel
from .substance import Substance


class Microorganism(CommonModel, WithComments):
    class Meta:
        verbose_name = "micro-organisme"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_genre = models.TextField(verbose_name="genre de micro-organisme (selon la base SICCRF)")
    ca_genre = models.TextField(verbose_name="genre de micro-organisme")
    genre = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_genre"), Value("")), F("siccrf_genre")),
        output_field=models.TextField(verbose_name="genre de micro-organisme"),
        db_persist=True,
    )
    substances = models.ManyToManyField(Substance, through="MicroorganismSubstanceRelation")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete", "genre"])

    @property
    def name_en(self):
        return self.siccrf_name_en


class MicroorganismSubstanceRelation(TimeStampable, Historisable):
    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée au micro-organisme (selon la base SICCRF)"
    )
    ca_is_related = models.BooleanField(null=True, default=None, verbose_name="substance associée au micro-organisme")


class MicroorganismSynonym(TimeStampable, Historisable, WithMissingImportBoolean):
    class Meta:
        verbose_name = "synonyme de micro-organisme"

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    standard_name = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
    name = models.TextField(verbose_name="nom")
    siccrf_is_obsolete = models.BooleanField(verbose_name="objet obsolète selon SICCRF", default=False)

    @property
    def is_obsolete(self):
        return self.siccrf_is_obsolete
