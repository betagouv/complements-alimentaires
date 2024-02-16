from django.db import models

from .mixins import WithSICCRFComments
from .abstract_models import SICCRFCommonModel
from .substance import Substance


class Ingredient(SICCRFCommonModel, WithSICCRFComments):
    """
    """
    class Meta:
        verbose_name = "autre ingrédient"
        verbose_name_plural = "autres ingrédients"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_observation = models.TextField(blank=True)
    siccrf_description = models.TextField(blank=True)
    siccrf_description_en = models.TextField(blank=True)
    siccrf_substances = models.ManyToManyField(Substance)


class IngredientSynonym(SICCRFCommonModel):
    class Meta:
        verbose_name = "synonyme d'ingrédient"

    standard_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
