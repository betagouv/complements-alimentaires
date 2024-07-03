from django.db import models


class IngredientActivity(models.IntegerChoices):
    """
    Les activités sont des IntegerChoices, car les Integer choisis pour chaque choix sont utilisés comme id dans les tables SICCRF
    Ce sont des équivalents de siccrf_id, qu'il ne faut donc pas modifier si on veut s'assurer de la cohérence des données.
    """

    ACTIVE = 1, "actif"
    NOT_ACTIVE = 0, "non actif"
