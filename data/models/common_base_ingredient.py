from django.db import models


class CommonBaseIngredient(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    public_comments = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Commentaires publics")
    private_comments = models.CharField(max_length=2000, null=True, blank=True, verbose_name="Commentaires privés")
    is_obsolete = models.BooleanField(verbose_name="Ingrédient obsolète")

    # commentaire_public_en = models.CharField(max_length=1000, blank=True)
    # commentaire_privé_en = models.CharField(max_length=2000, blank=True)  # TODO : intégrer les quelques données ici
    # ordre = models.IntegerField()
