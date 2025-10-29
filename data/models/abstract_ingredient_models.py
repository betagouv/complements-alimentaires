from django.core.exceptions import ValidationError
from django.db import models

# cette librairie permets d'avoir un affichage de l'arrayfield plus friendly dans l'admin
from django_jsonform.models.fields import ArrayField

from data.behaviours import TimeStampable
from data.choices import IngredientActivity

from .ingredient_status import WithStatus
from .mixins import WithComments, WithDefaultFields, WithIsRiskyBoolean, WithNovelFoodBoolean
from .unit import Unit


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

    warnings_on_label = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
        verbose_name="mention(s) d'avertissement devant figurer sur l'étiquette",
    )
    description = models.TextField(blank=True)
    # must_specify_quantity
    must_specify_quantity = models.BooleanField(
        default=False, verbose_name="spécification de quantité obligatoire lors de la déclaration ?"
    )

    unit = models.ForeignKey(
        Unit,
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="unité des quantités spécifiées (quantité max, apport de référence)",
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

    def _validate_unit_if_must_specify_quantity(self):
        if (not self.unit) & self.must_specify_quantity:
            raise ValidationError("L'unité doit être spécifiée si la quantité est nécessaire à la déclaration.")

    def save(self, *args, **kwargs):
        # blank = True permet de ne pas renseigner d'unité dans l'admin
        if not self.unit:
            self.unit = None
        self._validate_unit_if_must_specify_quantity()
        super().save(*args, **kwargs)
