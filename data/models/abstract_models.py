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
    history = HistoricalRecords(inherit=True)
    siccrf_id = models.IntegerField(blank=True, null=True, editable=False, db_index=True, unique=True)
    # ce champ permet de garder une trace des objets créés parce qu'ils sont dans une relation mais pour lesquels il manque les données réelles
    missing_import_data = models.BooleanField(blank=True, null=True, editable=False, default=False)
    # ordre = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def object_type(self):
        return self.__class__.__name__.lower()
