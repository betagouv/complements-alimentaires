from django.db import models


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
    name = models.TextField(default="", verbose_name="nom")

    is_obsolete = models.BooleanField(verbose_name="objet obsolète", default=False)


class WithComments(models.Model):
    """
    Les tables ingrédients (plantes, micro-organismes, substances et ingrédients de la SICCRF) portent 4 champs de commentaires.
    Les siccrf_public_comments contiennent les informations non sourcées scientifiquement.
    Les siccrf_public_comments_en et siccrf_private_comments_en, prévus pour être en anglais sont des champs très peu remplis.
    """

    class Meta:
        abstract = True

    public_comments = models.TextField(blank=True, verbose_name="commentaires publics")

    private_comments = models.TextField(blank=True, verbose_name="commentaires privés")

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

    is_novel_food = models.BooleanField(default=False, verbose_name="considéré Novel Food ?")


class WithWarning(models.Model):
    """
    Les tables ingrédients (plantes, micro-organismes, substances et ingrédients de la SICCRF) peuvent nécessiter l'inscription d'avertissements sur l'étiquette
    """

    class Meta:
        abstract = True

    warning = models.TextField(blank=True, editable=False, verbose_name="avertissement")


class PublicReasonHistoricalModel(models.Model):
    history_public_change_reason = models.CharField(
        blank=True, max_length=100, verbose_name="Raison de changement (public)"
    )

    class Meta:
        abstract = True
