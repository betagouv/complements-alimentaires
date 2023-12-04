from django.db import models


class Microorganism(models.Model):
    class Meta:
        verbose_name = "Micro-organisme"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name="Espèce de micro-organisme")
    public_comments = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Commentaires publics")
    private_comments = models.CharField(max_length=2000, null=True, blank=True, verbose_name="Commentaires privés")
    genre = models.CharField(max_length=200, verbose_name="Genre de micro-organisme")

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # commentaire_public_en = models.CharField(max_length=1000, blank=True)
    # commentaire_privé_en = models.CharField(max_length=2000, blank=True)
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class MicroorganismSynonym(models.Model):
    class Meta:
        verbose_name = "Synonymes de micro-organisme"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
