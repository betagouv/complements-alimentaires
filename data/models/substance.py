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

    @property
    def name_en(self):
        return self.siccrf_name_en

    @property
    def cas_number(self):
        return self.CA_cas_number if self.CA_cas_number else self.siccrf_cas_number
    
    @property
    def einec_number(self):
        return self.CA_einec_number if self.CA_einec_number else self.siccrf_einec_number

    @property
    def source(self):
        return self.CA_source if self.CA_source else self.siccrf_source

    @property
    def must_specify_quantity(self):
        return self.CA_must_specify_quantity if self.CA_must_specify_quantity else self.siccrf_must_specify_quantity

    @property
    def max_quantity(self):
        return self.CA_max_quantity if self.CA_max_quantity else self.siccrf_max_quantity

    @property
    def nutritional_reference(self):
        return self.CA_nutritional_reference if self.CA_nutritional_reference else self.siccrf_nutritional_reference

    
class SubstanceSynonym(CommonModel):
    class Meta:
        verbose_name = "synonyme substance active"

    standard_name = models.ForeignKey(Substance, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
