from django.db import models

from .mixins import WithCreationAndModificationDate, WithHistory, WithCAComments, WithSICCRFComments
from .abstract_models import CommonModel
from .substance import Substance


class PlantFamily(CommonModel):
    class Meta:
        verbose_name = "famille de plantes"
        verbose_name_plural = "familles de plantes"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")

    @property
    def name_en(self):
        return self.siccrf_name_en


class PlantPart(CommonModel):
    class Meta:
        verbose_name = "partie de plante"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")

    @property
    def name_en(self):
        return self.siccrf_name_en


class Plant(CommonModel, WithSICCRFComments, WithCAComments):
    class Meta:
        verbose_name = "plante"

    siccrf_family = models.ForeignKey(PlantFamily, null=True, on_delete=models.SET_NULL, verbose_name="famille de plante (selon la base SICCRF)", related_name="siccrf_plant_set")
    CA_family = models.ForeignKey(PlantFamily, null=True, on_delete=models.SET_NULL, verbose_name="famille de plante", related_name="plant_set")
    plant_parts = models.ManyToManyField(PlantPart, through="Part", verbose_name="partie de plante")
    substances = models.ManyToManyField(Substance, through="PlantSubstanceRelation")

    @property
    def family(self):
        return self.CA_family if self.CA_family else self.siccrf_family

    @family.setter
    def family(self, value):
        self.CA_family = value


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

    @property
    def must_be_monitored(self):
        return self.CA_must_be_monitored if self.CA_must_be_monitored else self.siccrf_must_be_monitored

    @must_be_monitored.setter
    def must_be_monitored(self, value):
        self.CA_must_be_monitored = value

    @property
    def is_useful(self):
        return self.CA_is_useful if self.CA_is_useful else self.siccrf_is_useful

    @is_useful.setter
    def is_useful(self, value):
        self.CA_is_useful = value


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
