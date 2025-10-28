from django.db import models
from django_jsonform.models.fields import ArrayField


class IngredientStatus(models.IntegerChoices):
    """
    Les status sont des IntegerChoices, car les Integer choisis
    pour chaque choix sont utilisés comme id dans les tables SICCRF
    Ce sont des équivalents de siccrf_id, qu'il ne faut donc pas modifier
    si on veut s'assurer de la cohérence des données.
    """

    AUTHORIZED = 1, "autorisé"  # contient aussi les status SICCRF "à inscrire" et "sans objet"
    NOT_AUTHORIZED = 2, "non autorisé"
    NO_STATUS = 3, "sans objet"
    AUTHORIZATION_REVOKED = 99, "retiré par l'administration"  # integer sans équivalent siccrf_id


class WithStatus(models.Model):
    """Mixins pour les ingrédients qui portent un statut règlementaire.
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
        blank=True,
        default=None,  # un ingrédient n'a pas de status par défaut
        null=True,
        verbose_name="statut de l'ingrédient ou substance",
    )

    to_be_entered_in_next_decree = models.BooleanField(
        default=False, verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?"
    )

    # ces liens justifient le statut
    regulatory_resource_links = ArrayField(
        base_field=models.URLField(), blank=True, null=True, verbose_name="Lien(s) vers les ressources reglementaires"
    )

    origin_declaration = models.ForeignKey(
        "data.Declaration",
        verbose_name="La déclaration qui a demandé la création de cet ingrédient",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    revoked_detail = models.TextField(blank=True, verbose_name="information pour les pros du retrait de l'ingrédient")
