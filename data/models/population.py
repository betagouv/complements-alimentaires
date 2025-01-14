from django.db import models

from simple_history.models import HistoricalRecords

from .abstract_models import CommonModel


class Population(CommonModel):
    class PopulationCategory(models.TextChoices):
        AGE = "AGE", "âge"
        MEDICAL = "MEDICAL", "conditions médicales spécifiques"
        PREGNANCY = "PREGNANCY", "grossesse et allaitement"
        OTHER = "OTHER", "autres"

    class Meta:
        verbose_name = "Population cible"
        verbose_name_plural = "Populations cibles"

    min_age = models.FloatField(blank=True, null=True, default=None)
    max_age = models.FloatField(blank=True, null=True, default=None)
    is_defined_by_anses = models.BooleanField(default=False)
    history = HistoricalRecords(inherit=True, excluded_fields=["name", "is_obsolete"])
    category = models.CharField(
        max_length=50,
        choices=PopulationCategory.choices,
        default=PopulationCategory.OTHER,
        verbose_name="categorie",
    )
