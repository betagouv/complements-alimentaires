from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Coalesce, NullIf


class WithMissingImportBoolean(models.Model):
    """
    Lors de l'import CSV certains objets peuvent être créés parce qu'ils sont dans une relation
    mais ils manquent dans ce cas de données informatives
    """

    class Meta:
        abstract = True

    missing_import_data = models.BooleanField(blank=True, null=True, editable=False, default=False)


class WithDefaultFields(models.Model):
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
    siccrf_name = models.TextField(editable=False, verbose_name="nom SICCRF")
    ca_name = models.TextField(blank=True, verbose_name="nom CA")
    name = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_name"), Value("")), F("siccrf_name")),
        output_field=models.TextField(verbose_name="nom"),
        db_persist=True,
    )

    siccrf_is_obsolete = models.BooleanField(editable=False, verbose_name="objet obsolète selon SICCRF", default=False)
    ca_is_obsolete = models.BooleanField(null=True, default=None, verbose_name="objet obsolète selon CA")
    is_obsolete = models.GeneratedField(
        expression=Coalesce(F("ca_is_obsolete"), F("siccrf_is_obsolete")),
        output_field=models.BooleanField(verbose_name="objet obsolète"),
        db_persist=True,
    )


class WithComments(models.Model):
    """
    Les tables ingrédients (plantes, micro-organismes, substances et ingrédients de la SICCRF) portent 4 champs de commentaires.
    Les siccrf_public_comments contiennent les informations non sourcées scientifiquement.
    Les siccrf_public_comments_en et siccrf_private_comments_en, prévus pour être en anglais sont des champs très peu remplis.
    """

    class Meta:
        abstract = True

    siccrf_public_comments = models.TextField(blank=True, editable=False, verbose_name="commentaires publics SICCRF")
    ca_public_comments = models.TextField(blank=True, verbose_name="commentaires publics CA")
    public_comments = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_public_comments"), Value("")), F("siccrf_public_comments")),
        output_field=models.TextField(verbose_name="commentaires publics"),
        db_persist=True,
    )

    siccrf_private_comments = models.TextField(blank=True, editable=False, verbose_name="commentaires privés SICCRF")
    ca_private_comments = models.TextField(blank=True, verbose_name="commentaires privés CA")
    private_comments = models.GeneratedField(
        expression=Coalesce(NullIf(F("ca_private_comments"), Value("")), F("siccrf_private_comments")),
        output_field=models.TextField(verbose_name="commentaires privés"),
        db_persist=True,
    )

    siccrf_public_comments_en = models.TextField(
        blank=True, editable=False, verbose_name="commentaires publics en anglais SICCRF"
    )
    siccrf_private_comments_en = models.TextField(
        blank=True, editable=False, verbose_name="commentaires privés en anglais SICCRF"
    )


class WithIsRiskyBoolean(models.Model):
    """
    Les tables ingrédients (plantes, micro-organismes, substances et ingrédients de la SICCRF) peuvent être considérés comme 'à risque'
    Cela implique notamment l'assignation d'un `article 15 vigilance`
    """

    class Meta:
        abstract = True

    is_risky = models.BooleanField(default=False, verbose_name="nécessite une instruction manuelle et vigilante ?")


class WithNovelFoodBoolean(models.Model):
    """
    Les tables ingrédients (plantes, micro-organismes, substances et ingrédients de la SICCRF) peuvent être considérés comme 'Novel Food'
    """

    class Meta:
        abstract = True

    novel_food = models.BooleanField(default=False, verbose_name="considéré Novel Food ?")


class PublicReasonHistoricalModel(models.Model):
    history_public_change_reason = models.CharField(
        blank=True, max_length=100, verbose_name="Raison de changement (public)"
    )

    class Meta:
        abstract = True
