from django.db import models

from .common_base_ingredient import CommonBaseIngredient
from .substance import Substance


class Microorganism(CommonBaseIngredient):
    class Meta:
        verbose_name = "micro-organisme"

    genre = models.TextField(verbose_name="genre de micro-organisme")
    substances = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()


class MicroorganismSynonym(models.Model):
    class Meta:
        verbose_name = "synonyme de micro-organisme"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField(verbose_name="nom")
    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
