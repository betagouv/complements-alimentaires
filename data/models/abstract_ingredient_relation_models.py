from django.db import models

from data.behaviours import Historisable, TimeStampable

from .population import Population


class SynonymType(models.TextChoices):
    SCIENTIFIC = "SCIENTIFIC_NAME", "Nom scientifique"  # TSYN[SBSTA,MO,AO]_IDENT=1 dans TeleIcare
    FRENCH = "FRENCH_NAME", "Nom en français"  # TSYN[SBSTA,MO,AO]_IDENT=2 dans TeleIcare
    ENGLISH = "ENGLISH_NAME", "Nom en anglais"  # TSYN[SBSTA,MO,AO]_IDENT=3 dans TeleIcare


class SynonymCommonModel(TimeStampable, Historisable):
    """
    Les modèles synonymes de tous les ingrédients héritent de ce modèle
    """

    class Meta:
        abstract = True

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    standard_name = None  # ce champ est défini dans les classes filles
    name = models.TextField(verbose_name="nom")
    synonym_type = models.CharField(
        choices=SynonymType.choices, default=SynonymType.FRENCH, verbose_name="type de synonyme"
    )

    def __str__(self):
        return self.name


class MaxQuantityPerPopulationRelationCommonModel(Historisable):
    """
    Les modèles MaxQuantityPerPopulationRelation de tous les ingrédients héritent de ce modèle
    """

    class Meta:
        abstract = True

    population = models.ForeignKey(Population, on_delete=models.CASCADE)

    max_quantity = models.FloatField(
        null=True,
        blank=True,
        verbose_name="quantité maximale autorisée pour la population cible",
    )
