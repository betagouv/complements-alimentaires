from django.db import models

from simple_history.models import HistoricalRecords

from .abstract_models import CommonModel


class Condition(CommonModel):
    class ConditionCategory(models.TextChoices):
        AGE = "AGE", "âge"
        MEDICAL = "MEDICAL", "conditions médicales spécifiques"
        PREGNANCY = "PREGNANCY", "grossesse et allaitement"
        MEDICAMENTS = "MEDICAMENTS", "interactions médicamenteuses"
        OTHER = "OTHER", "autres"

    class Meta:
        verbose_name = "condition de santé / facteurs de risque"

    siccrf_name_en = models.TextField(blank=True, verbose_name="nom en anglais selon la base SICCRF")
    min_age = models.FloatField(blank=True, null=True, default=None)
    max_age = models.FloatField(blank=True, null=True, default=None)
    history = HistoricalRecords(inherit=True)
    category = models.CharField(
        max_length=50,
        choices=ConditionCategory.choices,
        default=ConditionCategory.OTHER,
        verbose_name="categorie",
    )

    @property
    def name_en(self):
        return self.siccrf_name_en
