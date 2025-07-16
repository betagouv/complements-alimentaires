from django.db import models
from django.db.models import F, Value

from simple_history.models import HistoricalRecords

from data.behaviours import Historisable, TimeStampable

from .abstract_models import IngredientCommonModel
from .mixins import PublicReasonHistoricalModel
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


class MicroorganismSynonym(TimeStampable, Historisable):
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

    def __str__(self):
        return self.name
