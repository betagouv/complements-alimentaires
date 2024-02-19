from django.db import models

from .mixins import WithCreationAndModificationDate, WithHistory, WithSICCRFComments, WithCAComments
from .abstract_models import CommonModel
from .substance import Substance


class Ingredient(CommonModel, WithSICCRFComments, WithCAComments):
    """ """

    class Meta:
        verbose_name = "autre ingrédient"
        verbose_name_plural = "autres ingrédients"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_description = models.TextField(blank=True)
    substances = models.ManyToManyField(Substance, through="IngredientSubstanceRelation")

    @property
    def name_en(self):
        return self.siccrf_name_en

    @property
    def description(self):
        return self.siccrf_description


class IngredientSubstanceRelation(WithCreationAndModificationDate, WithHistory):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée à l'ingrédient (selon la base SICCRF)"
    )
    CA_is_related = models.BooleanField(null=True, default=None, verbose_name="substance associée à l'ingrédient")


class IngredientSynonym(CommonModel):
    class Meta:
        verbose_name = "synonyme d'ingrédient"

    standard_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
