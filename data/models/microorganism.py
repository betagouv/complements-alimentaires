from django.db import models

from .mixins import WithSICCRFComments
from .abstract_models import SICCRFCommonModel
from .substance import Substance


class Microorganism(SICCRFCommonModel, WithSICCRFComments):
    class Meta:
        verbose_name = "micro-organisme"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_genre = models.TextField(verbose_name="genre de micro-organisme")
    siccrf_substances = models.ManyToManyField(Substance)


class MicroorganismSynonym(SICCRFCommonModel):
    class Meta:
        verbose_name = "synonyme de micro-organisme"

    standard_name = models.ForeignKey(Microorganism, on_delete=models.CASCADE)
