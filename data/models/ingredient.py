from django.db import models

from .common_base_ingredient import CommonBaseIngredient
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


class IngredientSynonym(models.Model):
    class Meta:
        verbose_name = "synonyme d'ingrédient"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField(verbose_name="nom")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
