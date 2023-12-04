from django.db import models


class Substance(models.Model):
    class Meta:
        verbose_name = "substance active"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    public_comments = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Commentaires publics")
    private_comments = models.CharField(max_length=2000, blank=True, verbose_name="Commentaires privés")
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
    min_qty = models.CharField(
        max_length=2000, blank=True, verbose_name="Quantité minimale autorisée"
    )  # jamais remplie
    max_qty = models.CharField(max_length=2000, blank=True, verbose_name="Quantité maximale autorisée")
    nutritional_reference = models.CharField(
        max_length=2000, blank=True, verbose_name="Apport nutritionnel conseillé"
    )  # cette colonne devrat être associée à une unité

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # commentaire_public_en = models.CharField(max_length=1000, blank=True)
    # commentaire_privé_en = models.CharField(max_length=2000, blank=True) # TODO : intégrer les quelques données ici
    # source_en = models.CharField(max_length=1000, blank=True)
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class SubstanceSynonym(models.Model):
    class Meta:
        verbose_name = "Synonymes substance active"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
