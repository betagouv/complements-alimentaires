from django.db import models

from .abstract_models import CommonBaseIngredient, CommonBaseModel
from .substance import Substance


class PlantFamily(CommonBaseModel):
    class Meta:
        verbose_name = "famille de plantes"
        verbose_name_plural = "familles de plantes"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_id = models.IntegerField(blank=True, null=True, editable=False, db_index=True, unique=True)


class PlantPart(CommonBaseModel):
    class Meta:
        verbose_name = "partie de plante"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_id = models.IntegerField(blank=True, null=True, editable=False, db_index=True, unique=True)


class Plant(CommonBaseIngredient):
    class Meta:
        verbose_name = "plante"

    family = models.ForeignKey(PlantFamily, null=True, on_delete=models.SET_NULL, verbose_name="famille de plante")
    useful_parts = models.ManyToManyField(PlantPart)
    substances = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # to_watch_part = models.ManyToManyField(PlantPart)


class PlantSynonym(CommonBaseModel):
    class Meta:
        verbose_name = "synonyme de plante"

    standard_name = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TYSYN_IDENT en ForeignKeys
