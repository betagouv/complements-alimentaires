from django.db import models

from data.behaviours import TimeStampable
from data.choices import IngredientActivity

from .ingredient_status import WithStatus
from .mixins import WithComments, WithDefaultFields, WithIsRiskyBoolean, WithMissingImportBoolean


# Remplace le manager par défaut pour filtrer tous les modèles ayant un champ `is_obsolete`
class CommonModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.avoid_obsolete = kwargs.pop("avoid_obsolete", False)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.avoid_obsolete:
            return super().get_queryset().filter(is_obsolete=False)
        return super().get_queryset().all()


class CommonModel(TimeStampable, WithMissingImportBoolean, WithDefaultFields):
    """
    Tous les modèles issus de la base de données TeleIcare héritent de ce modèle
    """

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    objects = CommonModelManager()
    up_to_date_objects = CommonModelManager(avoid_obsolete=True)


class IngredientCommonModel(CommonModel, WithComments, WithStatus, WithIsRiskyBoolean):
    """
    Les modèles ingrédients héritent de ce modèle
    """

    class Meta:
        abstract = True

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
