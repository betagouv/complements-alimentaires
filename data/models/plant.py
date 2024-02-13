from django.db import models
from simple_history.models import HistoricalRecords

from .mixins import WithComments
from .abstract_models import CommonBaseModel
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


class Plant(CommonBaseModel, WithComments):
    class Meta:
        verbose_name = "plante"

    family = models.ForeignKey(PlantFamily, null=True, on_delete=models.SET_NULL, verbose_name="famille de plante")
    plant_parts = models.ManyToManyField(PlantPart, through="Part", verbose_name="partie de plante")
    substances = models.ManyToManyField(Substance)

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()


class Part(models.Model):
    """Ce modèle permet d'associer des données supplémentaires à la relation ManyToMany
    plant_parts
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    plantpart = models.ForeignKey(PlantPart, on_delete=models.CASCADE)
    must_be_monitored = models.BooleanField(default=False, verbose_name="⚠️ à surveiller ?")
    is_useful = models.BooleanField(default=False, verbose_name="🍵 utile (selon la base SICCRF) ?")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)


class PlantSynonym(CommonBaseModel):
    class Meta:
        verbose_name = "synonyme de plante"

    standard_name = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TYSYN_IDENT en ForeignKeys
