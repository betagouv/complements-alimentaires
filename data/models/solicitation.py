from __future__ import annotations

from urllib.parse import urljoin

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from api.utils.urls import get_base_url
from data.utils.type_utils import all_true_or_all_false

from ..behaviours import AutoValidable, TimeStampable
from ..fields import MultipleChoiceField
from .company import Company, CompanyRoleClassChoices

User = get_user_model()


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

    @property
    def personal_message_for_mail(self) -> str:
        """Permet d'ajouter les messages personnels dans le corps d'un message d'email"""
        return f" Iel a ajouté ce message : «{self.personal_msg}»." if self.personal_msg else ""

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
        self.recipients.set(recipients)
        send_mail(
            subject="[Compl'Alim] Nouvelle demande de gestion d'une entreprise",
            message=f"{self.description} {self.personal_message_for_mail}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=self.recipients.values_list("email", flat=True),
        )

    @processable_action
    def accept(self, processor):
        self.company.supervisors.set(self.sender)
        send_mail(
            subject="[Compl'Alim] Votre demande de gestion a été acceptée",
            message=f"L'équipe Compl'Alim a accepté que vous deveniez gestionnaire de {self.company.social_name}. Vous pouvez vous connecter à la plateforme.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.sender.email],
        )

    @processable_action
    def refuse(self, processor):
        send_mail(
            subject="[Compl'Alim] Votre demande de gestion a été refusée",
            message=f"L'équipe Compl'Alim a refusé que vous deveniez gestionnaire de {self.company.social_name}. N'hésitez pas à nous contacter pour en savoir plus.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.sender.email],
        )


class CoSupervisionClaim(BaseSolicitation, models.Model):
    """Utilisateur existant qui demande les droits de gestionnaire pour une entreprise qui a déjà des gestionnaires."""

    class Meta:
        verbose_name = "demande de co-gestion"
        verbose_name_plural = "demandes de co-gestion"

    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="destinataires")
    company = models.ForeignKey(Company, verbose_name=Company._meta.verbose_name, on_delete=models.CASCADE)

    @property
    def description(self):
        return f"{self.sender.name} a demandé à devenir co-gestionnaire de l'entreprise {self.company.social_name}."

    def create_hook(self):
        recipients = self.company.supervisors.all()
        self.recipients.set(recipients)
        send_mail(
            subject="[Compl'Alim] Nouvelle demande de co-gestion",
            message=f"{self.description} {self.personal_message_for_mail} Veuillez vous rendre sur la plateforme (section : gestion des collaborateurs) pour traiter cette demande.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients.values_list("email", flat=True),
        )

    @processable_action
    def accept(self, processor):
        self.company.supervisors.add(self.sender)
        login_page_url = urljoin(get_base_url(), "connexion")
        send_mail(
            subject="[Compl'Alim] Votre demande de co-gestion a été acceptée",
            message=f"{processor.name} a accepté que vous deveniez gestionnaire de {self.company.social_name}. Vous pouvez <a href='{login_page_url}'>vous connecter</a> à la plateforme.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.sender.email],
        )

    @processable_action
    def refuse(self, processor):
        send_mail(
            subject="[Compl'Alim] Votre demande de co-gestion a été refusée",
            message=f"{processor.name} a refusé que vous deveniez gestionnaire de {self.company.social_name}. Contactez directement cette personne pour en savoir plus.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.sender.email],
        )


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
        create_account_page_url = urljoin(get_base_url(), "inscription") + f"?email={self.recipient_email}"
        send_mail(
            subject="[Compl'Alim] Invitation à créer votre compte",
            message=f"{self.description} {self.personal_message_for_mail} Veuillez vous rendre sur <a href='{create_account_page_url}'>la plateforme Compl'Alim</a> pour créer votre compte.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.recipient_email],
        )

    @processable_action
    def account_created(self, processor):
        """Action déclenchable par l'inscription de l'utilisateur"""
        for role_classname in self.roles:
            role_class = apps.get_model("data", role_classname)
            role_class.objects.get_or_create(company=self.company, user=processor)
        send_mail(
            subject=f"[Compl'Alim] {processor.name} vous a rejoint en tant que collaborateur.",
            message=f"Suite à votre invitation, {processor.name} est devenu colloborateur de votre entreprise {self.company.social_name}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.sender.email],
        )
