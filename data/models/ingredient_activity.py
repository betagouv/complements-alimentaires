from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce


class IngredientActivity(models.IntegerChoices):
    """
    Les activités sont des IntegerChoices, car les Integer choisis pour chaque choix sont utilisés comme id dans les tables SICCRF
    Ce sont des équivalents de siccrf_id, qu'il ne faut donc pas modifier si on veut s'assurer de la cohérence des données.
    """

    ACTIVE = 1, "actif"
    NOT_ACTIVE = 0, "non actif"


class WithActivity(models.Model):
    """Mixins pour les ingrédients "(plantes, micro-organismes, substances et ingrédients de la SICCRF)" qui portent une activité biologique/biochimique.
    Cette mixins ne se trouve pas dans le fichier mixins pour éviter les imports circulaires.
    """

    class Meta:
        abstract = True

    siccrf_activity = models.IntegerField(
        choices=IngredientActivity.choices,
        null=True,
        verbose_name="activité de l'ingrédient selon TeleIcare",
    )
    ca_activity = models.IntegerField(
        choices=IngredientActivity.choices,
        null=True,
        verbose_name="activité de l'ingrédient selon Compl'Alim",
    )
    activity = models.GeneratedField(
        expression=Coalesce(F("ca_activity"), F("siccrf_activity")),
        output_field=models.IntegerField(
            choices=IngredientActivity.choices, null=True, verbose_name="activité de l'ingrédient"
        ),
        db_persist=True,
    )
