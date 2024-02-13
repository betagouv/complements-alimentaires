from django.db import models
from simple_history.models import HistoricalRecords


class WithComments(models.Model):
    class Meta:
        abstract = True

    public_comments = models.TextField(blank=True, verbose_name="commentaires publics")
    private_comments = models.TextField(blank=True, verbose_name="commentaires privés")

    # commentaire_public_en = models.TextField(blank=True)
    # commentaire_privé_en = models.TextField(blank=True)  # TODO : intégrer les quelques données ici


class WithCreationAndModificationDate(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


class WithHistory(models.Model):
    class Meta:
        abstract = True
    
    history = HistoricalRecords(inherit=True)


class SICCRFIngredientModel(models.Model):
    class Meta:
        abstract = True

    siccrf_id = models.IntegerField(blank=True, null=True, editable=False, db_index=True, unique=True)
    siccrf_name = models.TextField(verbose_name="nom")
    siccrf_is_obsolete = models.BooleanField(verbose_name="objet obsolète", default=False)
    # ce champ permet de garder une trace des objets créés parce qu'ils sont dans une relation mais pour lesquels il manque les données réelles
    siccrf_missing_import_data = models.BooleanField(blank=True, null=True, editable=False, default=False)
