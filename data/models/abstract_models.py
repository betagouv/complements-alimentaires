from django.db import models

from data.behaviours import TimeStampable

from .mixins import WithDefaultFields, WithMissingImportBoolean


class IngredientActivity(models.IntegerChoices):
    """
    Les activités sont des IntegerChoices, car les Integer choisis pour chaque choix sont utilisés comme id dans les tables SICCRF
    Ce sont des équivalents de siccrf_id, qu'il ne faut donc pas modifier si on veut s'assurer de la cohérence des données.
    """

    ACTIVE = 1, "actif"
    NOT_ACTIVE = 0, "non actif"


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
            "substances": IngredientActivity.ACTIVE,
            "non_active_ingredient": IngredientActivity.NOT_ACTIVE,
            # selon la règlementation, arome et additif sont des améliorants
            "aroma": IngredientActivity.NOT_ACTIVE,
            "additive": IngredientActivity.NOT_ACTIVE,
        }
        return TYPE_ACTIVITY_MAPPING[self.object_type]
