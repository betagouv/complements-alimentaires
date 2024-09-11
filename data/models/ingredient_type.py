from django.db import models


class IngredientType(models.IntegerChoices):
    """
    Les types sont des IntegerChoices, car les Integer choisis pour chaque
    choix sont utilisés comme id dans les tables SICCRF.
    Ce sont des équivalents de siccrf_id, qu'il ne faut donc pas modifier si
    on veut s'assurer de la cohérence des données.
    """

    FORM_OF_SUPPLY = (
        1,
        "Nutriment (Forme d'apport)",
    )
    ADDITIVE = 2, "Additif"
    AROMA = 3, "Arôme"  # TODO les arômes devraient peut-être disparaître à terme car tous non actifs
    ACTIVE_INGREDIENT = 4, "Autre ingrédient actif"
    NON_ACTIVE_INGREDIENT = 5, "Autre ingrédient"
