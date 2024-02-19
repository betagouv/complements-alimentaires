from django.db import models

from .mixins import WithCreationAndModificationDate, WithHistory, WithCAComments, WithSICCRFComments
from .abstract_models import CommonModel
from .substance import Substance


class PlantFamily(CommonModel):
    class Meta:
        verbose_name = "famille de plantes"
        verbose_name_plural = "familles de plantes"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")



class PlantPart(CommonModel):
    class Meta:
        verbose_name = "partie de plante"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")


class Plant(CommonModel, WithSICCRFComments, WithCAComments):
    class Meta:
        verbose_name = "plante"

    siccrf_family = models.ForeignKey(PlantFamily, null=True, on_delete=models.SET_NULL, verbose_name="famille de plante")
    CA_family = models.ForeignKey(PlantFamily, null=True, on_delete=models.SET_NULL, verbose_name="famille de plante")
    plant_parts = models.ManyToManyField(PlantPart, through="Part", verbose_name="partie de plante")
    substances = models.ManyToManyField(Substance, through="PlantSubstanceRelation")


class Part(WithCreationAndModificationDate, WithHistory):
    """
    Ce modèle permet d'associer des données supplémentaires à la relation ManyToMany
    plant_parts
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    plantpart = models.ForeignKey(PlantPart, on_delete=models.CASCADE)
    siccrf_must_be_monitored = models.BooleanField(default=False, verbose_name="⚠️ à surveiller (selon la base SICCRF) ?")
    CA_must_be_monitored = models.BooleanField(default=False, verbose_name="⚠️ à surveiller ?")
    siccrf_is_useful = models.BooleanField(default=False, verbose_name="🍵 utile (selon la base SICCRF) ?")
    CA_is_useful = models.BooleanField(default=False, verbose_name="🍵 utile ?")


class PlantSubstanceRelation(WithCreationAndModificationDate, WithHistory):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(default=False, verbose_name="substance associée à la plante (selon la base SICCRF)")
    CA_is_related = models.BooleanField(default=False, verbose_name="substance associée à la plante")


class PlantSynonym(CommonModel):
    class Meta:
        verbose_name = "synonyme de plante"

    standard_name = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TYSYN_IDENT en ForeignKeys
