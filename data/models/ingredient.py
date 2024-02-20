from django.db import models

from .mixins import (
    WithCreationAndModificationDate,
    WithHistory,
    WithMissingImportBoolean,
    WithSICCRFComments,
    WithCAComments,
)
from .abstract_models import CommonModel
from .substance import Substance


class Ingredient(CommonModel, WithSICCRFComments, WithCAComments):
    class Meta:
        verbose_name = "autre ingrédient"
        verbose_name_plural = "autres ingrédients"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_description = models.TextField(blank=True)
    substances = models.ManyToManyField(Substance, through="IngredientSubstanceRelation")

    @property
    def description(self):
        return self.siccrf_description


class IngredientSubstanceRelation(WithCreationAndModificationDate, WithHistory):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée à l'ingrédient (selon la base SICCRF)"
    )
    CA_is_related = models.BooleanField(default=False, verbose_name="substance associée à l'ingrédient")


class IngredientSynonym(WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean):
    class Meta:
        verbose_name = "synonyme d'ingrédient"

    standard_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
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
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
