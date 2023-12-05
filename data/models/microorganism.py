from django.db import models

from .common_base_ingredient import CommonBaseIngredient
from .substance import Substance


class Microorganism(CommonBaseIngredient):
    class Meta:
        verbose_name = "Micro-organisme"

    genre = models.CharField(max_length=200, verbose_name="Genre de micro-organisme")
    substance = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()


class MicroorganismSynonym(models.Model):
    class Meta:
        verbose_name = "Synonymes de micro-organisme"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
