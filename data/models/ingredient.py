from django.db import models

from .abstract_models import CommonBaseIngredient, CommonBaseModel
from .substance import Substance


class Ingredient(CommonBaseIngredient):
    class Meta:
        verbose_name = "autre ingrédient"
        verbose_name_plural = "autres ingrédients"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    observation = models.TextField(blank=True)
    description = models.TextField(blank=True)
    substances = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # stingsbs = models.IntegerField()
    # taing = models.IntegerField()
    # fctingr = models.IntegerField()
    # description_en = models.CharField(max_length=1000, blank=True)


class IngredientSynonym(CommonBaseModel):
    class Meta:
        verbose_name = "synonyme d'ingrédient"

    standard_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
