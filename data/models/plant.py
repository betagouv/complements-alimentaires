from django.db import models
from simple_history.models import HistoricalRecords

from .abstract_models import CommonBaseIngredient, CommonBaseModel
from .substance import Substance


class PlantFamily(CommonBaseModel):
    class Meta:
        verbose_name = "famille de plantes"
        verbose_name_plural = "familles de plantes"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")


class PlantPart(CommonBaseModel):
    class Meta:
        verbose_name = "partie de plante"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")


class Plant(CommonBaseIngredient):
    class Meta:
        verbose_name = "plante"

    family = models.ForeignKey(PlantFamily, null=True, on_delete=models.SET_NULL, verbose_name="famille de plante")
    useful_parts = models.ManyToManyField(PlantPart, through="UsefulPartRelation", verbose_name="partie utile")
    substances = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()


class UsefulPartRelation(models.Model):
    """Ce modèle permet d'associer des données supplémentaires à la relation ManyToMany
    useful_parts
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    plantpart = models.ForeignKey(PlantPart, on_delete=models.CASCADE)
    must_be_monitored = models.BooleanField(default=False, verbose_name="⚠️ à surveiller ?")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)


class PlantSynonym(CommonBaseModel):
    class Meta:
        verbose_name = "synonyme de plante"

    standard_name = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TYSYN_IDENT en ForeignKeys
