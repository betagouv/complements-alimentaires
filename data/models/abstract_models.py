from django.db import models

from data.behaviours import TimeStampable
from data.choices import IngredientActivity

from .mixins import WithDefaultFields, WithMissingImportBoolean


# Remplace le manager par défaut pour filtrer tous les modèles ayant un champ `is_obsolete`
class CommonModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_obsolete=False)


class CommonModel(TimeStampable, WithMissingImportBoolean, WithDefaultFields):
    """
    Les modèles ingrédients et les synonymes héritent de ce modèle
    """

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

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

    objects = CommonModelManager()
