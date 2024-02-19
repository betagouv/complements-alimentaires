from django.db import models

from .mixins import WithSICCRFComments, WithCAComments
from .abstract_models import CommonModel


class Substance(CommonModel, WithSICCRFComments, WithCAComments):
    """
    siccrf_min_quantity présente dans les tables SICCRF n'est strictement jamais remplie, donc pas transformée en champ du modèle
    siccrf_source_en présente dans les tables SICCRF est très peu remplie, donc pas transformée en champ du modèle
    """
    class Meta:
        verbose_name = "substance active"
        verbose_name_plural = "substances actives"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    siccrf_cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS")
    CA_cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS")
    siccrf_einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    CA_einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    siccrf_source = models.TextField(blank=True)
    CA_source = models.TextField(blank=True)
    siccrf_must_specify_quantity = models.BooleanField(default=False, verbose_name="spécification de quantité obligatoire")
    CA_must_specify_quantity = models.BooleanField(default=False, verbose_name="spécification de quantité obligatoire")
    siccrf_max_quantity = models.FloatField(null=True, blank=True, verbose_name="quantité maximale autorisée")
    CA_max_quantity = models.FloatField(null=True, blank=True, verbose_name="quantité maximale autorisée")
    siccrf_nutritional_reference = models.FloatField(
        null=True, blank=True, verbose_name="apport nutritionnel conseillé"
    )
    CA_nutritional_reference = models.FloatField(
        null=True, blank=True, verbose_name="apport nutritionnel conseillé"
    )  # cette colonne devrat être associée à une unité


    
class SubstanceSynonym(CommonModel):
    class Meta:
        verbose_name = "synonyme substance active"

    standard_name = models.ForeignKey(Substance, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
