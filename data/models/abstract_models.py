from django.contrib.postgres.fields import ArrayField
from django.db import models

from data.behaviours import TimeStampable
from data.choices import IngredientActivity

from .ingredient_status import WithStatus
from .mixins import WithComments, WithDefaultFields, WithIsRiskyBoolean, WithNovelFoodBoolean


class SynonymType(models.TextChoices):
    SCIENTIFIC = "SCIENTIFIC_NAME", "Nom scientifique"  # TSYN[SBSTA,MO,AO]_IDENT=1 dans TeleIcare
    FRENCH = "FRENCH_NAME", "Nom en français"  # TSYN[SBSTA,MO,AO]_IDENT=2 dans TeleIcare
    ENGLISH = "ENGLISH_NAME", "Nom en anglais"  # TSYN[SBSTA,MO,AO]_IDENT=3 dans TeleIcare


# Remplace le manager par défaut pour filtrer tous les modèles ayant un champ `is_obsolete`
class CommonModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.avoid_obsolete = kwargs.pop("avoid_obsolete", False)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.avoid_obsolete:
            return super().get_queryset().exclude(is_obsolete=True)
        return super().get_queryset().all()


class CommonModel(TimeStampable, WithDefaultFields):
    """
    Tous les modèles issus de la base de données TeleIcare héritent de ce modèle
    """

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    objects = CommonModelManager()
    up_to_date_objects = CommonModelManager(avoid_obsolete=True)


class IngredientCommonModel(CommonModel, WithComments, WithStatus, WithIsRiskyBoolean, WithNovelFoodBoolean):
    """
    Les modèles ingrédients héritent de ce modèle
    """

    class Meta:
        abstract = True

    origin_declaration = models.ForeignKey(
        "data.Declaration",
        verbose_name="La déclaration qui a demandé la création de cet ingrédient",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    requires_analysis_report = models.BooleanField(
        default=False, verbose_name="L'utilisation de cet ingrédient nécessite un bulletin d'analyse"
    )

    regulatory_resource_links = ArrayField(
        base_field=models.URLField(), blank=True, null=True, verbose_name="Lien(s) vers les ressources reglementaires"
    )

    @property
    def object_type(self):
        """
        Dans la base SICCRF, l'activité d'un ingrédient :
        * était stockée dans une colonne `fctingr`
        * était assignée à chaque ingrédient individuellement.
        Nous avons découvert que les activités ne dépendent fait que du type d'ingrédient.
        """
        return self.__class__.__name__.lower()

    @property
    def activity(self):
        """
        Dans la base SICCRF, l'activité d'un ingrédient :
        * était stockée dans une colonne `fctingr`
        * était assignée à chaque ingrédient individuellement.
        Nous avons découvert que les activités ne dépendent fait que du type d'ingrédient.
        """
        TYPE_ACTIVITY_MAPPING = {
            "plant": IngredientActivity.ACTIVE,
            "microorganism": IngredientActivity.ACTIVE,
            "form_of_supply": IngredientActivity.ACTIVE,
            "active_ingredient": IngredientActivity.ACTIVE,
            # Dans TeleIcare, les substances n'avaient pas de champ activity associé
            "substance": IngredientActivity.ACTIVE,
            "non_active_ingredient": IngredientActivity.NOT_ACTIVE,
            # selon la règlementation, arome et additif sont des améliorants
            "aroma": IngredientActivity.NOT_ACTIVE,
            "additive": IngredientActivity.NOT_ACTIVE,
        }
        return TYPE_ACTIVITY_MAPPING[self.object_type]
