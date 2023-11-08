from django.db import models
from simple_history.models import HistoricalRecords
from .approvalstate import LegacyApprovalState

class Plant(models.Model):

    class Meta:
        verbose_name = "plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    # Legacy fields
    legacy_latin_name = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom de la plante en latin")
    legacy_synonym = models.TextField(null=True, blank=True, verbose_name="(Legacy) Nom synonyme")
    legacy_useful_part = models.TextField(null=True, blank=True, verbose_name="(Legacy) Partie utile")
    legacy_surveillance_part = models.TextField(null=True, blank=True, verbose_name="(Legacy) Partie à surveiller")
    legacy_active_substances = models.TextField(null=True, blank=True, verbose_name="(Legacy) Substances actives")
    legacy_approval_state = models.CharField(
        max_length=255,
        choices=LegacyApprovalState.choices,
        null=True,
        blank=True,
        verbose_name="(Legacy) Status d'approbation",
    )
    legacy_family = models.TextField(null=True, blank=True, verbose_name="(Legacy) Famille de plante")
    legacy_function = models.TextField(null=True, blank=True, verbose_name="(Legacy) Fonction de la plante - ingrédient")
    legacy_public_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires publics")
    legacy_private_comments = models.TextField(null=True, blank=True, verbose_name="(Legacy) Commentaires privés")
