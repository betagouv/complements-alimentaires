from django.db import models

from .mixins import WithCreationAndModificationDate, WithHistory, WithSICCRFComments
from .abstract_models import SICCRFCommonModel
from .substance import Substance


class Microorganism(SICCRFCommonModel, WithSICCRFComments):
    class Meta:
        verbose_name = "micro-organisme"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_genre = models.TextField(verbose_name="genre de micro-organisme")
    substances = models.ManyToManyField(Substance, through="MicroorganismSubstanceRelation")


class MicroorganismSubstanceRelation(WithCreationAndModificationDate, WithHistory):
    microorganism = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)
    siccrf_is_related = models.BooleanField(
        default=False, verbose_name="substance associée au micro-organisme (selon la base SICCRF)"
    )
    CA_is_related = models.BooleanField(null=True, default=None, verbose_name="substance associée au micro-organisme")


class MicroorganismSynonym(SICCRFCommonModel):
    class Meta:
        verbose_name = "synonyme de micro-organisme"

    standard_name = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
