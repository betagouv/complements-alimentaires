from django.db import models
from django.db.models.functions import Coalesce, NullIf
from django.db.models import F, Value

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

    # CAS number
    siccrf_cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS (selon la base SICCRF)")
    CA_cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS")
    cas_number = models.GeneratedField(
        expression=Coalesce(NullIf(F("CA_cas_number"), Value("")), F("siccrf_cas_number")),
        output_field=models.CharField(max_length=10, blank=True, verbose_name="numéro CAS"),
        db_persist=True,
    )

    # EINECS number
    siccrf_einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS (selon la base SICCRF)",
    )
    CA_einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    einec_number = models.GeneratedField(
        expression=Coalesce(NullIf(F("CA_einec_number"), Value("")), F("siccrf_einec_number")),
        output_field=models.CharField(max_length=7, blank=True, verbose_name="numéro EINECS"),
        db_persist=True,
    )

    # source
    siccrf_source = models.TextField(blank=True)
    CA_source = models.TextField(blank=True)
    source = models.GeneratedField(
        expression=Coalesce(NullIf(F("CA_source"), Value("")), F("siccrf_source")),
        output_field=models.TextField(),
        db_persist=True,
    )

    # must_specify_quantity
    siccrf_must_specify_quantity = models.BooleanField(
        default=False,
        verbose_name="spécification de quantité obligatoire (selon la base SICCRF)",
    )
    CA_must_specify_quantity = models.BooleanField(default=False, verbose_name="spécification de quantité obligatoire")
    must_specify_quantity = models.GeneratedField(
        expression=Coalesce(F("CA_must_specify_quantity"), F("siccrf_must_specify_quantity")),
        output_field=models.BooleanField(default=False, verbose_name="spécification de quantité obligatoire"),
        db_persist=True,
    )

    # max_quantity
    siccrf_max_quantity = models.FloatField(
        null=True,
        blank=True,
        verbose_name="quantité maximale autorisée (selon la base SICCRF)",
    )
    CA_max_quantity = models.FloatField(null=True, blank=True, verbose_name="quantité maximale autorisée")
    max_quantity = models.GeneratedField(
        expression=Coalesce(F("CA_max_quantity"), F("siccrf_max_quantity")),
        output_field=models.FloatField(null=True, blank=True, verbose_name="spécification de quantité obligatoire"),
        db_persist=True,
    )

    # nutritional_reference
    # TODO: cette colonne devrat être associée à une unité
    siccrf_nutritional_reference = models.FloatField(
        null=True,
        blank=True,
        verbose_name="apport nutritionnel conseillé (selon la base SICCRF)",
    )
    CA_nutritional_reference = models.FloatField(null=True, blank=True, verbose_name="apport nutritionnel conseillé")
    nutritional_reference = models.GeneratedField(
        expression=Coalesce(F("CA_nutritional_reference"), F("siccrf_nutritional_reference")),
        output_field=models.FloatField(null=True, blank=True, verbose_name="apport nutritionnel conseillé"),
        db_persist=True,
    )


class SubstanceSynonym(CommonModel):
    class Meta:
        verbose_name = "synonyme substance active"

    standard_name = models.ForeignKey(Substance, on_delete=models.CASCADE, verbose_name="nom de référence")
    # TODO importer aussi les synonym_type = TSYNSBSTA_IDENT en ForeignKeys
