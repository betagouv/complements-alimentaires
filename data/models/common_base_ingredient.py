from django.db import models


class CommonBaseIngredient(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField(verbose_name="nom")
    name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    public_comments = models.TextField(blank=True, verbose_name="commentaires publics")
    private_comments = models.TextField(blank=True, verbose_name="commentaires privés")
    is_obsolete = models.BooleanField(verbose_name="ingrédient obsolète")

    # commentaire_public_en = models.TextField(blank=True)
    # commentaire_privé_en = models.TextField(blank=True)  # TODO : intégrer les quelques données ici
    # ordre = models.IntegerField()
