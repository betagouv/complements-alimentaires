from django.db import models
from django.db.models.functions import Coalesce, NullIf
from django.db.models import F, Value

from simple_history.models import HistoricalRecords

from data.behaviours import TimeStampable, Historisable
from .mixins import WithMissingImportBoolean, WithComments
from .abstract_models import CommonModel
from .substance import Substance


# cette fonction remplace le fonction Concat qui est mutable avec PSQL
# les GeneratedFields doivent avoir des expression de génération immutables
# Avec Django 5.1 ce problème sera résolu https://forum.djangoproject.com/t/using-generatedfield-with-postgres/27224/4
class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"


class Microorganism(CommonModel, WithComments):
    class Meta:
        verbose_name = "micro-organisme"

    # réécriture des champs provenant de la mixin WithDefaultFields
    # le champ name n'existe pas dans la base SICCRF il est calculé à partir du genre et de l'espèce
    siccrf_name = None
    ca_name = None
    name = models.GeneratedField(
        expression=ConcatOp(
            Coalesce(NullIf(F("ca_genus"), Value("")), F("siccrf_genus")),
            Value(" "),
            Coalesce(NullIf(F("ca_species"), Value("")), F("siccrf_species")),
        ),
        output_field=models.TextField(verbose_name="nom"),
        db_persist=True,
    )

    siccrf_genus = models.TextField(verbose_name="genre de micro-organisme (selon la base SICCRF)")
    ca_genus = models.TextField(verbose_name="genre de micro-organisme")
    genus = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_genus"), Value("")), F("siccrf_genus")),
        output_field=models.TextField(verbose_name="genre de micro-organisme"),
        db_persist=True,
    )
    siccrf_species = models.TextField(verbose_name="espèce de micro-organisme (selon la base SICCRF)")
    ca_species = models.TextField(verbose_name="espèce de micro-organisme")
    species = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_species"), Value("")), F("siccrf_species")),
        output_field=models.TextField(verbose_name="espèce de micro-organisme"),
        db_persist=True,
    )

    substances = models.ManyToManyField(Substance, through="MicroorganismSubstanceRelation")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete", "genus", "species"])


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
