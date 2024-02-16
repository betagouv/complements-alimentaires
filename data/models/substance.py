from django.db import models

from .mixins import WithSICCRFComments
from .abstract_models import SICCRFCommonModel


class Substance(SICCRFCommonModel, WithSICCRFComments):
    class Meta:
        verbose_name = "substance active"
        verbose_name_plural = "substances actives"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS")
    siccrf_einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    siccrf_source = models.TextField(blank=True)
    siccrf_source_en = models.TextField(blank=True)
    siccrf_must_specify_quantity = models.BooleanField(default=False, verbose_name="spécification de quantité obligatoire")
    siccrf_min_quantity = models.FloatField(
        null=True, blank=True, verbose_name="quantité minimale autorisée"
    )  # jamais remplie
    siccrf_max_quantity = models.FloatField(null=True, blank=True, verbose_name="quantité maximale autorisée")
    siccrf_nutritional_reference = models.FloatField(
        null=True, blank=True, verbose_name="apport nutritionnel conseillé"
    )  # cette colonne devrat être associée à une unité


class SubstanceSynonym(SICCRFCommonModel):
    class Meta:
        verbose_name = "synonyme substance active"

    standard_name = models.ForeignKey(Substance, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
