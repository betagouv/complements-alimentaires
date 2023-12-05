from django.db import models


class Population(models.Model):
    class Meta:
        verbose_name = (
            "Groupe de population (cible d'un complément ou à risque d'un ingrédient/substance ou d'un complément)"
        )

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)

    # ces champs semblent inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class Condition(models.Model):
    class Meta:
        verbose_name = "Condition de santé impliquant des facteurs de risque"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
