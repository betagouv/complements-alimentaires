from django.db import models


class SubstanceUnit(models.Model):
    class Meta:
        verbose_name = "unité"

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    name = models.CharField(max_length=3, verbose_name="unité", unique=True)
    long_name = models.TextField(verbose_name="unité détaillée")

    def __str__(self):
        return f"{self.long_name} ({self.name})"
