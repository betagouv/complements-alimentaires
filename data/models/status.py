from django.db import models


class IngredientStatus(models.IntegerChoices):
    AUTHORIZED = 1, "autorisé"
    NOT_AUTHORIZED = 2, "non autorisé"
    PENDING_REGISTRATION = 3, "à inscrire"
    NA = 4, "sans objet"

    __empty__ = "inconnu"  # TODO: devrait-on merger "sans objet" et "inconnu" ?


class WithStatus(models.Model):
    """Mixins pour les ingrédients "(plantes, micro-organismes, substances et ingrédients de la SICCRF)" qui portent un statut.
    C'est le statut de leur autorisation dans les compléments alimentaires.
    Cette mixins ne se trouve pas dans le fichier mixins pour éviter les imports circulaires.
    On ne fait pas 2 champs un siccrf_ un ca_ car c'est un champ spécifiquement voué a évoluer.
    """

    class Meta:
        abstract = True

    status = models.IntegerField(
        choices=IngredientStatus.choices,
        null=True,
        verbose_name="statut de l'ingrédient ou substance",
    )
