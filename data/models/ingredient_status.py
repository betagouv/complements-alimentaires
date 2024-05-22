from django.db import models


class IngredientStatus(models.IntegerChoices):
    """
    Les status sont des IntegerChoices, car les Integer choisis
    pour chaque choix sont utilisés comme id dans les tables SICCRF
    Ce sont des équivalents de siccrf_id, qu'il ne faut donc pas modifier
    si on veut s'assurer de la cohérence des données.
    """

    AUTHORIZED = 1, "autorisé"  # contient aussi les status SICCRF "à inscrire" et "sans objet"
    NOT_AUTHORIZED = 2, "non autorisé"


class WithStatus(models.Model):
    """Mixins pour les ingrédients qui portent un statut.
    (plantes, micro-organismes, substances, arômes, additifs, formes d'apport)
    C'est le statut de leur autorisation dans les compléments alimentaires.
    Cette mixins ne se trouve pas dans le fichier mixins pour éviter
    les imports circulaires.
    On ne fait pas 2 champs un siccrf_ un ca_ car c'est un champ
    spécifiquement voué a évoluer.
    """

    class Meta:
        abstract = True

    status = models.IntegerField(
        choices=IngredientStatus.choices,
        default=2,  # un ingrédient est non autorisé par défaut
        null=True,
        verbose_name="statut de l'ingrédient ou substance",
    )
    to_be_entered_in_next_decree = models.BooleanField(
        editable=False, default=0, verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?"
    )
