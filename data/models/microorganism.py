from django.db import models
from django.db.models.functions import Coalesce, NullIf
from django.db.models import F, Value

from simple_history.models import HistoricalRecords

from .mixins import WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean, WithComments
from .abstract_models import CommonModel
from .substance import Substance


class Microorganism(CommonModel, WithComments):
    class Meta:
        verbose_name = "micro-organisme"

    # réécriture des champs provenant de la mixin WithDefaultFields
    # le champ name n'existe pas dans la base SICCRF il est calculé à partir du genre et de l'espèce
    siccrf_name = None
    ca_name = None
    name = models.GeneratedField(
        expression=Coalesce(
            Coalesce(NullIf(F("ca_genre"), Value("")), F("siccrf_genre")),
            Coalesce(NullIf(F("ca_espece"), Value("")), F("siccrf_espece")),
        ),
        output_field=models.TextField(verbose_name="nom"),
        db_persist=True,
    )

    siccrf_genre = models.TextField(verbose_name="genre de micro-organisme (selon la base SICCRF)")
    ca_genre = models.TextField(verbose_name="genre de micro-organisme")

    siccrf_espece = models.TextField(verbose_name="espèce de micro-organisme (selon la base SICCRF)")
    ca_espece = models.TextField(verbose_name="espèce de micro-organisme")

    substances = models.ManyToManyField(Substance, through="MicroorganismSubstanceRelation")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete", "genre"])


class MicroorganismSubstanceRelation(WithCreationAndModificationDate, WithHistory):
    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée au micro-organisme (selon la base SICCRF)"
    )
    ca_is_related = models.BooleanField(null=True, default=None, verbose_name="substance associée au micro-organisme")


class MicroorganismSynonym(WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean):
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
