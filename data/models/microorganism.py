from django.db import models

from .abstract_models import CommonBaseIngredient, CommonBaseModel
from .substance import Substance


class Microorganism(CommonBaseIngredient):
    class Meta:
        verbose_name = "micro-organisme"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    genre = models.TextField(verbose_name="genre de micro-organisme")
    substances = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()


class MicroorganismSynonym(CommonBaseModel):
    class Meta:
        verbose_name = "synonyme de micro-organisme"

    standard_name = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
