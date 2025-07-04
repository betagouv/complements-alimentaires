from django.db import models

from simple_history.models import HistoricalRecords

from data.behaviours import TimeStampable

from .abstract_models import CommonModelManager


class Population(TimeStampable):
    class PopulationCategory(models.TextChoices):
        AGE = "AGE", "âge"
        PREGNANCY = "PREGNANCY", "grossesse et allaitement"
        OTHER = "OTHER", "autres"

    class Meta:
        verbose_name = "Population cible"
        verbose_name_plural = "Populations cibles"

    name = models.TextField(blank=True, verbose_name="nom")

    is_obsolete = models.BooleanField(null=True, default=None, verbose_name="objet obsolète selon CA")

    min_age = models.FloatField(blank=True, null=True, default=None)
    max_age = models.FloatField(blank=True, null=True, default=None)
    is_defined_by_anses = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True)
    category = models.CharField(
        max_length=50,
        choices=PopulationCategory.choices,
        default=PopulationCategory.OTHER,
        verbose_name="categorie",
    )

    def __str__(self):
        return self.name

    objects = CommonModelManager()
    up_to_date_objects = CommonModelManager(avoid_obsolete=True)
