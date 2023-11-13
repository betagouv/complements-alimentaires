from django.db import models
from simple_history.models import HistoricalRecords
from .approvalstate import LegacyApprovalState


class Substance(models.Model):
    class Meta:
        verbose_name = "substance active"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # Legacy fields
    legacy_sbsact_name = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom SBSACT")
    legacy_synonym = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom synonyme")
    legacy_type = models.TextField(null=True, blank=True, verbose_name="(Legacy) Type")
    legacy_approval_state = models.CharField(
        max_length=255,
        choices=LegacyApprovalState.choices,
        null=True,
        blank=True,
        verbose_name="(Legacy) Status d'approbation",
    )
    legacy_public_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires publics")
    legacy_private_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires privés")
    legacy_source = models.TextField(null=True, blank=True, verbose_name="(Legacy) Substance source")
