from django.db import models
from django.db.models.functions import Coalesce

from simple_history.models import HistoricalRecords


class WithCreationAndModificationDate(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class WithHistory(models.Model):
    class Meta:
        abstract = True

    history = HistoricalRecords(inherit=True)


class WithMissingImportBoolean(models.Model):
    """
    Lors de l'import CSV certains objets peuvent être créés parce qu'ils sont dans une relation
    mais ils manquent dans ce cas de données informatives
    """

    class Meta:
        abstract = True

    missing_import_data = models.BooleanField(
        blank=True, null=True, editable=False, default=False
    )


class WithSICCRFDefaultFields(models.Model):
    class Meta:
        abstract = True

    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="id dans les tables et tables relationnelles SICCRF",
    )
    siccrf_name = models.TextField(verbose_name="nom SICCRF")
    siccrf_is_obsolete = models.BooleanField(
        verbose_name="objet obsolète selon SICCRF", default=False
    )


class WithSICCRFComments(models.Model):
    """
    Les tables ingrédients (plantes, micro-organismes, substances et ingrédients de la SICCRF) portent 4 champs de commentaires.
    Les siccrf_public_comments contiennent les informations non sourcées scientifiquement.
    Les siccrf_public_comments_en et siccrf_private_comments_en, prévus pour être en anglais sont des champs très peu remplis.
    """

    class Meta:
        abstract = True

    siccrf_public_comments = models.TextField(
        blank=True, editable=False, verbose_name="commentaires publics SICCRF"
    )
    siccrf_private_comments = models.TextField(
        blank=True, editable=False, verbose_name="commentaires privés SICCRF"
    )
    siccrf_public_comments_en = models.TextField(
        blank=True,
        editable=False,
        verbose_name="commentaires publics en anglais SICCRF",
    )
    siccrf_private_comments_en = models.TextField(
        blank=True, editable=False, verbose_name="commentaires privés en anglais SICCRF"
    )


class WithCADefaultFields(models.Model):
    class Meta:
        abstract = True

    CA_name = models.TextField(verbose_name="nom CA")
    CA_is_obsolete = models.BooleanField(
        verbose_name="objet obsolète selon CA", default=False
    )

    name = models.GeneratedField(
        expression=Coalesce("CA_name", "siccrf_name"),
        output_field=models.TextField(verbose_name="nom"),
        db_persist=True,
    )

    is_obsolete = models.GeneratedField(
        expression=Coalesce("CA_is_obsolete", "siccrf_is_obsolete"),
        output_field=models.TextField(verbose_name="objet obsolète"),
        db_persist=True,
    )


class WithCAComments(models.Model):
    class Meta:
        abstract = True

    CA_public_comments = models.TextField(
        blank=True, verbose_name="commentaires publics SICCRF"
    )
    CA_private_comments = models.TextField(
        blank=True, verbose_name="commentaires privés SICCRF"
    )

    @property
    def public_comments(self):
        return (
            self.CA_public_comments
            if self.CA_public_comments
            else self.siccrf_public_comments
        )

    @property
    def private_comments(self):
        return (
            self.CA_private_comments
            if self.CA_private_comments
            else self.siccrf_private_comments
        )
