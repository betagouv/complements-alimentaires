from django.db import models
from simple_history.models import HistoricalRecords

from data.behaviours import TimeStampable, Historisable
from .mixins import WithMissingImportBoolean, WithComments
from .abstract_models import CommonModel
from .substance import Substance


class Ingredient(CommonModel, WithComments):
    class Meta:
        verbose_name = "autre ingrédient"
        verbose_name_plural = "autres ingrédients"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_description = models.TextField(blank=True)
    substances = models.ManyToManyField(Substance, through="IngredientSubstanceRelation")
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete"])

    @property
    def name_en(self):
        return self.siccrf_name_en

    @property
    def description(self):
        return self.siccrf_description


class IngredientSubstanceRelation(TimeStampable, Historisable):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée à l'ingrédient (selon la base SICCRF)"
    )
    ca_is_related = models.BooleanField(null=True, default=None, verbose_name="substance associée à l'ingrédient")


class IngredientSynonym(TimeStampable, Historisable, WithMissingImportBoolean):
    class Meta:
        verbose_name = "synonyme d'ingrédient"

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
    siccrf_is_obsolete = models.BooleanField(verbose_name="objet obsolète selon SICCRF", default=False)
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys

    @property
    def is_obsolete(self):
        return self.siccrf_is_obsolete
