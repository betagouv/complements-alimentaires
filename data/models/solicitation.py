from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models, transaction
from django.utils import timezone

from data.utils.type_utils import all_true_or_all_false

from ..behaviours import AutoValidable, TimeStampable

User = get_user_model()


class SolicitationKindChoices(models.TextChoices):
    """Fait aussi office de mapping avec les classes contenant la logique spécifique à appeler"""

    RequestSupervisionSolicitation = "RequestSupervisionSolicitation", "demande de gestion"
    RequestCoSupervisionSolicitation = "RequestCoSupervisionSolicitation", "demande de co-gestion"
    InviteCoSupervision = "InviteCoSupervision", "invitation à une co-gestion"


class CustomSolicitationManager(models.Manager):
    @transaction.atomic
    def create(self, *args, **kwargs) -> Solicitation:
        """Délègue la création de l'objet à une sous-classe"""
        subclass = globals()[kwargs["kind"]]  # récupère la sous-classe à partir du type
        instance = subclass.create_hook(*args, **kwargs)
        if not isinstance(instance, Solicitation):
            raise ValueError("`create_hook` method must return a new Solicitation instance")
        return instance


class Solicitation(AutoValidable, TimeStampable, models.Model):
    """
    Objet permettant de définir les invitations ou demandes envoyées.
    Il gère aussi le traitement de ces demandes (ex : acceptation, refus)
    """

    objects = CustomSolicitationManager()

    class Meta:
        verbose_name = "solicitation"
        ordering = ("-creation_date",)

    kind = models.CharField(choices=SolicitationKindChoices, verbose_name="type")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="émetteur", on_delete=models.PROTECT, related_name="solicitations_sent"
    )
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name="destinataires", related_name="solicitations_received"
    )
    description = models.TextField()
    processed_at = models.DateTimeField(blank=True, null=True, verbose_name="traité à")
    processor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="traité par",
        default=None,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="solicitations_processed",
    )
    processed_action = models.CharField(blank=True, verbose_name="action de traitement")

    @property
    def is_processed(self) -> bool:
        return bool(self.processed_at)

    def clean(self):
        if not all_true_or_all_false(self.processed_at, self.processor, self.processed_action):
            raise ValidationError("Une demande traitée doit l'être par quelqu'un ET à une date spécifiée")

    def save(self, *args, **kwargs):
        # if not self._state.adding and self.is_processed:
        #     raise ValidationError("Une demande traitée ne peut plus être modifiée")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}"

    @property
    def subclass(self):
        """Récupère la classe permettant de gérer la logique de traitement spécifique"""
        return globals().get(self.kind)

    @transaction.atomic
    def process(self, action: str, processor, *args, **kwargs) -> None:
        """Marque une demande comme traitée et appelle l'action de traitement spécifique"""

        self.processor = processor
        self.processed_at = timezone.now()
        self.processed_action = action
        self.save()
        # l'action de traitement est déléguée
        process_action_method = getattr(self.subclass, action, None)
        if process_action_method:
            process_action_method(solicitation=self, processor=processor, *args, **kwargs)
        else:
            raise NotImplementedError(f"The action {action} does not exist on {self.subclass} class.")

    def accept(self, processor, *args, **kwargs):
        """Sucre pour l'action `accept`"""
        return self.process(action="accept", processor=processor, *args, **kwargs)

    def refuse(self, processor, *args, **kwargs):
        """Sucre pour l'action `refuse`"""
        return self.process(action="refuse", processor=processor, *args, **kwargs)


class RequestSupervisionSolicitation:
    @staticmethod
    def create_hook(kind, sender, company_social_name, company_id, identifier_type, identifier) -> Solicitation:
        main_message = f"{sender.name} (id: {sender.id}) a demandé à devenir gestionnaire de l'entreprise {company_social_name} dont le N° de {identifier_type} est {identifier}."
        new_solicitation = Solicitation(kind=kind, sender=sender, description=main_message)
        new_solicitation.save()
        new_solicitation.recipients.add(*User.objects.filter(is_staff=True))
        send_mail(
            subject="Nouvelle demande d'accès à une entreprise (sans gestionnaire)",
            message=main_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return new_solicitation

    @staticmethod
    def accept(solicitation, processor, company) -> None:
        send_mail(
            subject="Votre demande de gestion a été acceptée",
            message=f"{solicitation.processor.name} de l'équipe Compl'Alim a accepté que vous deveniez gestionnaire de {company.social_name}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[solicitation.sender],
        )

    @staticmethod
    def refuse(solicitation, processor, company) -> None:
        send_mail(
            subject="Votre demande de gestion a été refusée",
            message=f"{solicitation.processor.name} de l'équipe Compl'Alim a refusé que vous deveniez gestionnaire de {company.social_name}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[solicitation.sender],
        )
