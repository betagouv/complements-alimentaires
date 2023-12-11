from django.db import models
from simple_history.models import HistoricalRecords


class CommonBaseModel(models.Model):
    """
    This meta class is used for Synonyms as well as other simple models
    """

    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.TextField(verbose_name="nom")
    is_obsolete = models.BooleanField(verbose_name="objet obsolète", default=False)
    history = HistoricalRecords()
    # ordre = models.IntegerField()

    def __str__(self):
        return self.name


class CommonBaseIngredient(CommonBaseModel):
    class Meta:
        abstract = True

    name_en = models.TextField(blank=True, verbose_name="nom en anglais")
    public_comments = models.TextField(blank=True, verbose_name="commentaires publics")
    private_comments = models.TextField(blank=True, verbose_name="commentaires privés")

    # commentaire_public_en = models.TextField(blank=True)
    # commentaire_privé_en = models.TextField(blank=True)  # TODO : intégrer les quelques données ici
