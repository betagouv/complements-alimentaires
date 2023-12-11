from django.db import models

from .common_base_ingredient import CommonBaseIngredient


class Substance(CommonBaseIngredient):
    class Meta:
        verbose_name = "substance active"
        verbose_name_plural = "substances actives"

    cas_number = models.CharField(max_length=10, blank=True, verbose_name="numéro CAS")
    einec_number = models.CharField(
        max_length=7,
        blank=True,
        verbose_name="numéro EINECS",
    )
    source = models.TextField(blank=True)
    must_specify_quantity = models.BooleanField()
    min_quantity = models.FloatField(blank=True, verbose_name="quantité minimale autorisée")  # jamais remplie
    max_quantity = models.FloatField(blank=True, verbose_name="quantité maximale autorisée")
    nutritional_reference = models.FloatField(
        blank=True, verbose_name="apport nutritionnel conseillé"
    )  # cette colonne devrat être associée à une unité

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # source_en = models.TextField(blank=True)


class SubstanceSynonym(models.Model):
    class Meta:
        verbose_name = "synonyme substance active"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField()
    substance = models.ForeignKey(Substance, on_delete=models.CASCADE)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
    # TSYN -> est-ce que ça donne l'ordre d'affichage des synonymes ?
