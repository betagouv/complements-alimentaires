from django.db import models

from .mixins import WithComments
from .abstract_models import CommonBaseModel


class Substance(CommonBaseModel, WithComments):
    class Meta:
        verbose_name = "substance active"
        verbose_name_plural = "substances actives"

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS")
    einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    source = models.TextField(blank=True)
    must_specify_quantity = models.BooleanField(default=False, verbose_name="spécification de quantité obligatoire")
    min_quantity = models.FloatField(
        null=True, blank=True, verbose_name="quantité minimale autorisée"
    )  # jamais remplie
    max_quantity = models.FloatField(null=True, blank=True, verbose_name="quantité maximale autorisée")
    nutritional_reference = models.FloatField(
        null=True, blank=True, verbose_name="apport nutritionnel conseillé"
    )  # cette colonne devrat être associée à une unité

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # source_en = models.TextField(blank=True)


class SubstanceSynonym(CommonBaseModel):
    class Meta:
        verbose_name = "synonyme substance active"

    standard_name = models.ForeignKey(Substance, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
