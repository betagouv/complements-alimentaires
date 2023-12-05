from django.db import models

from .common_base_ingredient import CommonBaseIngredient


class Substance(CommonBaseIngredient):
    class Meta:
        verbose_name = "substance active"

    cas_number = models.CharField(
        max_length=10, blank=True, verbose_name="Numéro CAS (Chemical Abstracts Service) - Standard mondial"
    )
    einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="Numéro EINECS (Inventaire européen des substances chimiques commerciales existantes)",
    )
    source = models.CharField(max_length=1000, blank=True)
    qty_to_fill = models.BooleanField()
    min_qty = models.FloatField(blank=True, verbose_name="Quantité minimale autorisée")  # jamais remplie
    max_qty = models.FloatField(blank=True, verbose_name="Quantité maximale autorisée")
    nutritional_reference = models.FloatField(
        blank=True, verbose_name="Apport nutritionnel conseillé"
    )  # cette colonne devrat être associée à une unité

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # source_en = models.CharField(max_length=1000, blank=True)


class SubstanceSynonym(models.Model):
    class Meta:
        verbose_name = "Synonymes substance active"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
    # TSYN -> est-ce que ça donne l'ordre d'affichage des synonymes ?
