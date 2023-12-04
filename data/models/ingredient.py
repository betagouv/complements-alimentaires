from django.db import models


class Ingredient(models.Model):
    class Meta:
        verbose_name = "Autre ingrédient"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    observation = models.CharField(max_length=200, blank=True)
    public_comments = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Commentaires publics")
    private_comments = models.CharField(max_length=2000, null=True, blank=True, verbose_name="Commentaires privés")
    description = models.CharField(max_length=1000, blank=True)

    # champs présents dans le CSV mais inutilisés
    # stingsbs = models.IntegerField()
    # taing = models.IntegerField()
    # fctingr = models.IntegerField()
    # commentaire_public_en = models.CharField(max_length=1000, blank=True)
    # commentaire_privé_en = models.CharField(max_length=2000, blank=True)  # TODO : intégrer les quelques données ici
    # description_en = models.CharField(max_length=1000, blank=True)
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class IngredientSynonym(models.Model):
    class Meta:
        verbose_name = "Synonymes d'ingrédient"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
