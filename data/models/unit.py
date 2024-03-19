from django.db import models
from .mixins import WithMissingImportBoolean


class SubstanceUnit(WithMissingImportBoolean):
    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    name = models.CharField(max_length=2, verbose_name="unité")
    long_name = models.TextField(verbose_name="unité détaillée")
