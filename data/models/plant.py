from django.db import models

from .abstract_models import CommonBaseIngredient, CommonBaseModel
from .substance import Substance


class Family(CommonBaseModel):
    class Meta:
        verbose_name = "famille de plantes"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")


class PlantPart(CommonBaseModel):
    class Meta:
        verbose_name = "partie de plante"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")


class Plant(CommonBaseIngredient):
    class Meta:
        verbose_name = "plante"

    family = models.ForeignKey(Family, on_delete=models.DO_NOTHING, verbose_name="famille de plante")
    useful_parts = models.ManyToManyField(PlantPart)
    substances = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # to_watch_part = models.ManyToManyField(PlantPart)


class PlantSynonym(CommonBaseModel):
    class Meta:
        verbose_name = "synonyme de plante"

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")
