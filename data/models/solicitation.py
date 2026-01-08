from __future__ import annotations

import logging

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from api.utils.urls import get_base_url
from config import email
from data.utils.type_utils import all_true_or_all_false

from ..behaviours import AutoValidable, TimeStampable
from ..fields import MultipleChoiceField
from .company import Company, CompanyRoleClassChoices

User = get_user_model()

logger = logging.getLogger(__name__)


def processable_action(func):
    """Décorateur pour traiter les solicitations automatiquement"""

    def wrapper(self, processor, *args, **kwargs):
        with transaction.atomic():
            self.processed_at = timezone.now()
            self.processor = processor
            self.processed_action = func.__name__
            self.save()
            return func(self, processor, *args, **kwargs)

    return wrapper


class BaseSolicitation(AutoValidable, TimeStampable):
    class Meta:
        abstract = True

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="émetteur", on_delete=models.PROTECT, related_name="%(class)s_sent"
    )
    personal_msg = models.TextField(blank=True, null=False, verbose_name="message personnel de l'émetteur (optionnel)")

    # Les champs ci-dessous concernent le traitement de la solicitation, et sont vide à la création
    processed_at = models.DateTimeField(
        blank=True, null=True, verbose_name="traité à"
    )  # par convention, on utilise ce champ parmi les 3 pour définir si l'objet a été traité ou pas
    processor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="traité par",
        default=None,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(class)s_processed",
    )
    processed_action = models.CharField(blank=True, verbose_name="action de traitement")

    def clean(self):
        if self._state.adding:
            if any([self.processed_at, self.processor, self.processed_action]):
                raise ValidationError("Des champs innatendus ont été définis lors de la création de l'objet.")

        if not all_true_or_all_false(self.processed_at, self.processor, self.processed_action):
            raise ValidationError(
                "Une demande traitée doit l'être par quelqu'un ET à une date spécifiée ET par une action spécifique."
            )

    def save(self, *args, **kwargs):
        """Surchargée pour appeler un hook optionnel à la création de l'objet, défini dans la classe enfant"""
        is_adding = self._state.adding
        super().save(*args, **kwargs)  # modifie self._state.adding, c'est pour ça qu'on l'a mis en variable avant
        if is_adding and hasattr(self, "create_hook"):
            self.create_hook()

    @property
    def description(self):
        raise NotImplementedError("Veuillez décrire cette property dans la classe enfant")

    def __str__(self):
        return self.description


class SupervisionClaim(BaseSolicitation, models.Model):
    """Utilisateur existant qui demande les droits de gestionnaire pour une entreprise qui n'en a pas encore."""

    class Meta:
        verbose_name = "demande de gestion"
        verbose_name_plural = "demandes de gestion"

    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="destinataires")
    company = models.ForeignKey(Company, verbose_name=Company._meta.verbose_name, on_delete=models.CASCADE)

    @property
    def description(self):
        return f"{self.sender.name} (id: {self.sender.id}) a demandé à devenir gestionnaire de l'entreprise {self.company.social_name} (id: {self.company.id}). "

    def create_hook(self):
        recipients = User.objects.filter(is_staff=True)
        self.recipients.set(recipients)  # TODO: Je ne pense pas que le self.recipients sert à quelque chose
        for recipient in recipients:
            try:
                email.send_sib_template(
                    email.EmailTemplateID.REQUEST_TO_JOIN_EMPTY_COMPANY.value,
                    {
                        "REQUESTER_NAME": self.sender.get_full_name(),
                        "COMPANY_NAME": self.company.social_name,
                        "COMPANY_ID": self.company.id,
                        "ADMIN_LINK": f"{get_base_url()}admin/",
                        "PERSONAL_MESSAGE": self.personal_msg,
                    },
                    recipient.email,
                    recipient.get_full_name(),
                )
            except Exception as e:
                logger.error(f"Email not sent on SupervisionClaim creation with id {self.id}")
                logger.exception(e)

    @processable_action
    def accept(self, processor):
        # TODO : cette action n'est jamais appelé de nulle part. Lors qu'elle le sera il faudra
        # créer un template Brevo
        self.company.supervisors.add(self.sender)
        send_mail(
            subject="[Compl'Alim] Votre demande de gestion a été acceptée",
            message=f"L'équipe Compl'Alim a accepté que vous deveniez gestionnaire de {self.company.social_name}. Vous pouvez vous connecter à la plateforme.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.sender.email],
        )

    @processable_action
    def refuse(self, processor):
        # TODO : cette action n'est jamais appelé de nulle part. Lors qu'elle le sera il faudra
        # créer un template Brevo
        send_mail(
            subject="[Compl'Alim] Votre demande de gestion a été refusée",
            message=f"L'équipe Compl'Alim a refusé que vous deveniez gestionnaire de {self.company.social_name}. N'hésitez pas à nous contacter pour en savoir plus.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.sender.email],
        )


class CompanyAccessClaim(BaseSolicitation, models.Model):
    """Utilisateur existant qui demande accès (gestionnaire ou déclarant)
    pour une entreprise qui a déjà des gestionnaires."""

    class Meta:
        verbose_name = "demande d'accès à une entreprise"
        verbose_name_plural = "demandes d'accès à une entreprise"

    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="destinataires")
    company = models.ForeignKey(Company, verbose_name=Company._meta.verbose_name, on_delete=models.CASCADE)
    declarant_role = models.BooleanField(default=False, verbose_name="demande de rôle déclarant")
    supervisor_role = models.BooleanField(default=False, verbose_name="demande de rôle gestionnaire")

    @property
    def description(self):
        role_string = ""
        if self.declarant_role and self.supervisor_role:
            role_string = "pour les rôles déclarant et gestionnaire."
        elif self.declarant_role:
            role_string = "pour le rôle déclarant."
        elif self.supervisor_role:
            role_string = "pour le rôle gestionnaire."
        return f"Demande d'accès à la compagnie {self.company.social_name} {role_string}"

    def create_hook(self):
        recipients = self.company.supervisors.all()
        self.recipients.set(recipients)
        for recipient in self.recipients.all():
            try:
                email.send_sib_template(
                    email.EmailTemplateID.REQUEST_TO_JOIN_COMPANY.value,
                    {
                        "REQUESTER_NAME": self.sender.get_full_name(),
                        "COMPANY_NAME": self.company.social_name,
                        "REQUEST_LINK": f"{get_base_url()}gestion-des-collaborateurs/{self.company.id}",
                        "PERSONAL_MESSAGE": self.personal_msg,
                    },
                    recipient.email,
                    recipient.get_full_name(),
                )
            except Exception as e:
                logger.error(f"Email not sent on CompanyAccessClaim creation with id {self.id}")
                logger.exception(e)

    @processable_action
    def accept(self, processor):
        if self.supervisor_role:
            self.company.supervisors.add(self.sender)
        if self.declarant_role:
            self.company.declarants.add(self.sender)

        try:
            email.send_sib_template(
                email.EmailTemplateID.ACCEPT_REQUEST_TO_JOIN_COMPANY.value,
                {
                    "REQUESTER_NAME": self.sender.get_full_name(),
                    "COMPANY_NAME": self.company.social_name,
                    "DASHBOARD_LINK": f"{get_base_url()}tableau-de-bord?company={self.company.id}",
                },
                self.sender.email,
                self.sender.get_full_name(),
            )
        except Exception as e:
            logger.error(f"Email not sent on CompanyAccessClaim accept action with id {self.id}")
            logger.exception(e)

    @processable_action
    def refuse(self, processor):
        try:
            email.send_sib_template(
                email.EmailTemplateID.REFUSE_REQUEST_TO_JOIN_COMPANY.value,
                {
                    "COMPANY_NAME": self.company.social_name,
                },
                self.sender.email,
                self.sender.get_full_name(),
            )
        except Exception as e:
            logger.error(f"Email not sent on CompanyAccessClaim refuse action with id {self.id}")
            logger.exception(e)


class CollaborationInvitation(BaseSolicitation, models.Model):
    """Invite une personne à créer un compte utilisateur, qui aura d'ores et déjà les rôles d'entreprise fournis"""

    class Meta:
        verbose_name = "invitation à devenir collaborateur"
        verbose_name_plural = "invitations à devenir collaborateur"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "recipient_email"],
                name="unique_collaboration_invitation",
                condition=Q(processed_at__isnull=True),  # s'applique uniquement sur les invitations non traitées
            )
        ]

    recipient_email = models.EmailField("adresse e-mail du destinataire")
    company = models.ForeignKey(Company, verbose_name=Company._meta.verbose_name, on_delete=models.CASCADE)
    roles = MultipleChoiceField(
        models.CharField(choices=CompanyRoleClassChoices), verbose_name="classes de rôle", default=list
    )

    @property
    def description(self):
        return f"{self.sender.name} vous invite à créer un compte Compl'Alim et rejoindre l'entreprise {self.company.social_name}."

    def create_hook(self):
        try:
            email.send_sib_template(
                email.EmailTemplateID.INVITE_TO_JOIN_COMPANY.value,
                {
                    "COMPANY_NAME": self.company.social_name,
                    "SENDER_NAME": self.sender.name,
                    "SIGNUP_LINK": f"{get_base_url()}inscription?email={self.recipient_email}",
                },
                self.recipient_email,
                self.recipient_email,
            )
        except Exception as e:
            logger.error(f"Email not sent on CollaborationInvitation creation with id {self.id}")
            logger.exception(e)

    @processable_action
    def account_created(self, processor):
        """Action déclenchable par l'inscription de l'utilisateur"""
        for role_classname in self.roles:
            role_class = apps.get_model("data", role_classname)
            role_class.objects.get_or_create(company=self.company, user=processor)

        try:
            email.send_sib_template(
                email.EmailTemplateID.COMPANY_INVITATION_ACCEPTED.value,
                {
                    "COMPANY_NAME": self.company.social_name,
                    "NEW_COLLABORATOR": processor.get_full_name(),
                    "MEMBERS_LINK": f"{get_base_url()}gestion-des-collaborateurs/{self.company.id}",
                },
                self.sender.email,
                self.sender.get_full_name(),
            )
        except Exception as e:
            logger.error(f"Email not sent on CollaborationInvitation account_created with id {self.id}")
            logger.exception(e)
