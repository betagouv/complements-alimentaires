import decimal

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from data.behaviours import TimeStampable

from .declaration import Declaration


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


class Snapshot(TimeStampable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="personne ayant effectué le changement",
        related_name="snapshots",
    )
    status = models.CharField(
        max_length=50,
        choices=Declaration.DeclarationStatus.choices,
        verbose_name="status",
    )
    declaration = models.ForeignKey(
        Declaration,
        on_delete=models.CASCADE,
        verbose_name="déclaration",
        related_name="snapshots",
    )
    expiration_days = models.IntegerField(null=True, blank=True, verbose_name="délai de réponse")
    json_declaration = models.JSONField(verbose_name="données au moment de la création", encoder=CustomJSONEncoder)
    comment = models.TextField("commentaire", blank=True, default="")
