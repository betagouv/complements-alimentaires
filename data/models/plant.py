from django.db import models

from .common_base_ingredient import CommonBaseIngredient
from .substance import Substance


class Family(models.Model):
    class Meta:
        verbose_name = "famille de plantes"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField(verbose_name="nom")
    name_en = models.TextField(blank=True, verbose_name="nom en anglais")

    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class PlantPart(models.Model):
    class Meta:
        verbose_name = "partie de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField(verbose_name="nom")
    name_en = models.TextField(blank=True, verbose_name="nom en anglais")

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class Plant(CommonBaseIngredient):
    class Meta:
        verbose_name = "plante"

    family = models.ForeignKey(Family, on_delete=models.DO_NOTHING, verbose_name="famille de plante")
    useful_parts = models.ManyToManyField(PlantPart)
    substance = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # to_watch_part = models.ManyToManyField(PlantPart)


class PlantSynonym(models.Model):
    class Meta:
        verbose_name = "synonyme de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField(verbose_name="nom synonyme")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
