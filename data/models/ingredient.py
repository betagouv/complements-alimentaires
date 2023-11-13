from django.db import models
from simple_history.models import HistoricalRecords
from .approvalstate import LegacyApprovalState


class Ingredient(models.Model):
    class Meta:
        verbose_name = "Autres ingrédients"

    class LegacyIngredientType(models.TextChoices):
        ADDITIVE = "additive", "Additif"
        SCENT = "scent", "Arôme"
        OTHER = "other", "Autre ingrédient"
        OTHER_ACTIVE = "other_active", "Autre ingrédient actif"
        NUTRIENT = "nutrient", "Nutriment"

    class LegacySynonymType(models.TextChoices):
        FRENCH = "french", "Nom français"
        SCIENTIFIC = "scientific", "Nom scientifique"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # Legacy fields
    legacy_name = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom")
    legacy_type = models.CharField(
        max_length=255,
        choices=LegacyIngredientType.choices,
        null=True,
        blank=True,
        verbose_name="(Legacy) Type",
    )
    legacy_synonym = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom synonyme")
    legacy_synonym_type = models.CharField(
        max_length=255,
        choices=LegacySynonymType.choices,
        null=True,
        blank=True,
        verbose_name="(Legacy) Synonym yype",
    )
    legacy_substance_name = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom de la substance")
    legacy_substance_unit_name = models.TextField(
        null=True, blank=True, verbose_name="(Legacy) Nom de la substance avec unité"
    )
    legacy_approval_state = models.CharField(
        max_length=255,
        choices=LegacyApprovalState.choices,
        null=True,
        blank=True,
        verbose_name="(Legacy) Status d'approbation",
    )
    legacy_intake_source = models.TextField(null=True, blank=True, verbose_name="(Legacy) Source d'apports")
    legacy_minimum_dose = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=5,
        verbose_name="(Legacy) Dose minimale",
    )
    legacy_maximum_dose = models.DecimalField(
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=5,
        verbose_name="(Legacy) Dose maximale",
    )
    legacy_public_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires publics")
    legacy_private_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires privés")
    legacy_observations = models.TextField(null=True, blank=True, verbose_name="(Legacy) Observations")
    legacy_description = models.TextField(null=True, blank=True, verbose_name="(Legacy) Description")
