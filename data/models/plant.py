from django.db import models

from .common_base_ingredient import CommonBaseIngredient
from .substance import Substance


class Family(models.Model):
    class Meta:
        verbose_name = "Famille de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)  # TODO : à vérifier une fois le CSV reçu
    name_en = models.CharField(max_length=200, blank=True)

    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class PlantPart(models.Model):
    class Meta:
        verbose_name = "Partie de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class Plant(CommonBaseIngredient):
    class Meta:
        verbose_name = "Plante"

    family = models.ForeignKey(Family, null=True, on_delete=models.SET_NULL, verbose_name="Famille de plante")
    useful_parts = models.ManyToManyField(PlantPart)
    substance = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # to_watch_part = models.ManyToManyField(PlantPart)


class PlantSynonym(models.Model):
    class Meta:
        verbose_name = "Synonymes de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
