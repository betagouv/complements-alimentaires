from django.db import models


class Population(models.Model):
    class Meta:
        verbose_name = "Population cible / à risque"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField()
    name_en = models.TextField(blank=True)

    # ces champs semblent inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class Condition(models.Model):
    class Meta:
        verbose_name = "condition de santé / facteurs de risque"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField()
    name_en = models.TextField(blank=True)
