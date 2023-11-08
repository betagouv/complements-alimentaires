from django.db import models
from simple_history.models import HistoricalRecords
from .approvalstate import LegacyApprovalState

class Microorganism(models.Model):
    
    class Meta:
        verbose_name = "micro-organisme"

    class LegacyMicroorganismStatus(models.TextChoices):
        UNKNOWN = "unknown", "Sans objet"
        AUTHORIZED = "authorized", "Autorisé"

    class LegacyMicroorganismFunction(models.TextChoices):
        ACTIVE = "active", "Actif"


    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # Legacy fields
    legacy_species_name = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom de l'espèce")
    legacy_genre_name = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom du genre")
    legacy_full_name = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom complet")
    legacy_approval_state = models.CharField(
        max_length=255,
        choices=LegacyApprovalState.choices,
        null=True,
        blank=True,
        verbose_name="(Legacy) Status d'approbation",
    )
    legacy_function = models.CharField(
        max_length=255,
        choices=LegacyMicroorganismFunction.choices,
        null=True,
        blank=True,
        verbose_name="(Legacy) Fonction",
    )
    legacy_public_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires publics")
    legacy_private_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires privés")
