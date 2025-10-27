import decimal

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
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
    class SnapshotActions(models.TextChoices):
        SUBMIT = "SUBMIT", "soumettre pour instruction"
        TAKE_FOR_INSTRUCTION = "TAKE_FOR_INSTRUCTION", "prendre pour instruction"
        OBSERVE_NO_VISA = "OBSERVE_NO_VISA", "mettre en observation sans visa"
        AUTHORIZE_NO_VISA = "AUTHORIZE_NO_VISA", "autoriser sans visa"
        RESPOND_TO_OBSERVATION = "RESPOND_TO_OBSERVATION", "répondre à une observation"
        RESPOND_TO_OBJECTION = "RESPOND_TO_OBJECTION", "répondre à une objection"
        REQUEST_VISA = "REQUEST_VISA", "demander un visa"
        TAKE_FOR_VISA = "TAKE_FOR_VISA", "prendre pour visa"
        ACCEPT_VISA = "APPROVE_VISA", "valider le visa"
        REFUSE_VISA = "REFUSE_VISA", "refuser le visa"
        WITHDRAW = "WITHDRAW", "retirer du marché"
        ABANDON = "ABANDON", "mettre en abandon"
        AUTOMATICALLY_AUTHORIZE = "AUTOMATICALLY_AUTHORIZE", "validé automatiquement par le bot"
        REVOKE_AUTHORIZATION = "REVOKE_AUTHORIZATION", "retirer du marché par l'administration"
        OTHER = "OTHER", "autre"

    action = models.CharField(
        max_length=50,
        blank=True,
        choices=SnapshotActions.choices,
        default=SnapshotActions.OTHER,
    )
    post_validation_status = models.CharField(
        max_length=50,
        blank=True,
        choices=Declaration.DeclarationStatus.choices,
        default=Declaration.DeclarationStatus.DRAFT,
        verbose_name="status à assigner après la validation",
    )
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
    blocking_reasons = ArrayField(
        models.TextField(), null=True, blank=True, verbose_name="raisons de la dernière décision défavorable"
    )
    effective_withdrawal_date = models.DateField("date effective de retrait du marché", blank=True, null=True)
