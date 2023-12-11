from django.db import models

from .abstract_models import CommonBaseIngredient, CommonBaseModel
from .substance import Substance


class Ingredient(CommonBaseIngredient):
    class Meta:
        verbose_name = "autre ingrédient"
        verbose_name_plural = "autres ingrédients"

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

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
