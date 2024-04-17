from django.db import models

from .mixins import WithMissingImportBoolean


class IngredientStatus(WithMissingImportBoolean):
    class Meta:
        verbose_name = (
            "statut de l'élément selon le décret 2006-352 du 20 mars 2006 relatif aux compléments alimentaires."
        )

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    name = models.TextField(verbose_name="statut")

    def __str__(self):
        return self.name


class WithStatus(models.Model):
    """Mixins pour les ingrédients "(plantes, micro-organismes, substances et ingrédients de la SICCRF)" qui portent un statut.
    C'est le statut de leur autorisation dans les compléments alimentaires.
    Cette mixins ne se trouve pas dans le fichier mixins pour éviter les imports circulaires.
    On ne fait pas 2 champs un siccrf_ un ca_ car c'est un champ spécifiquement voué a évoluer.
    """

    class Meta:
        abstract = True

    status = models.ForeignKey(
        IngredientStatus,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="statut de l'ingrédient ou substance",
        related_name="%(class)s_siccrf_status",
    )
