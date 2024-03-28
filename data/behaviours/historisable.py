from django.db import models
from simple_history.models import HistoricalRecords


class Historisable(models.Model):
    class Meta:
        abstract = True

    history = HistoricalRecords(inherit=True)
