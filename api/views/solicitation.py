import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils.urls import get_base_url
from config import email
from data.models import CollaborationInvitation, Company, CompanyAccessClaim

from ..exception_handling import ProjectAPIException
from ..permissions import IsSolicitationRecipient, IsSupervisor
from ..serializers import AddNewCollaboratorSerializer, CollaborationInvitationSerializer, CompanyAccessClaimSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


class CollaborationInvitationListView(ListAPIView):
    serializer_class = CollaborationInvitationSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company.objects.filter(supervisors=user), pk=self.kwargs["pk"])
        return CollaborationInvitation.objects.filter(company=company, processor__isnull=True)


class CompanyAccessClaimListView(ListAPIView):
    serializer_class = CompanyAccessClaimSerializer

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company.objects.filter(supervisors=user), pk=self.kwargs["pk"])
        return CompanyAccessClaim.objects.filter(recipients=user, company=company, processor__isnull=True)


class ProcessCompanyAccessClaim(APIView):
    """Effectue une action de traitement sur une demande d'accès'"""

    permission_classes = [IsSolicitationRecipient]

    def post(self, request, pk: int, *args, **kwargs):
        solicitation = get_object_or_404(CompanyAccessClaim, pk=pk)
        self.check_object_permissions(request, solicitation)
        action = getattr(solicitation, request.data.get("action_name", ""), None)
        if action:
            action(processor=request.user)
        else:
            raise ParseError()
        return Response({})


class AddNewCollaboratorView(APIView):
    """Ajout d'un collaborateur pouvant mener à différents cas (ajout des rôles, invitation par mail, erreurs)."""

    permission_classes = [IsSupervisor]

    @transaction.atomic
    def post(self, request, pk: int, *args, **kwargs):
        company = get_object_or_404(Company, pk=pk)
        self.check_object_permissions(request, company)

        serializer = AddNewCollaboratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipient_email = serializer.validated_data["recipient_email"]
        roles = serializer.validated_data["roles"]
        sender = request.user
        try:
            recipient = User.objects.get(email=recipient_email)
        except User.DoesNotExist:
            # Cas A : l'invité n'existe pas en base, mais une invitation non traitée a déjà été envoyée
            if CollaborationInvitation.objects.filter(
                company=company, recipient_email=recipient_email, processed_at__isnull=True
            ).exists():
                raise ProjectAPIException(
                    field_errors={"recipient_email": "Une invitation a déjà été envoyée à cette adresse e-mail."}
                )
            # Cas B : l'invité n'existe pas en base, et aucune invitation n'a été envoyée
            CollaborationInvitation.objects.create(
                sender=sender, company=company, recipient_email=recipient_email, roles=roles
            )
            return Response({"message": f"L'invitation a bien été envoyée à {recipient_email}."})
        else:
            # Cas C : l'invité existe en base et fait déjà partie des collaborateurs de l'entreprise
            if recipient in company.collaborators:
                raise ProjectAPIException(
                    field_errors={"recipient_email": "Cet utilisateur fait déjà partie de vos collaborateurs."}
                )
            # Cas D : l'invité existe en base mais n'est pas encore collaborateur de l'entreprise
            else:
                for role_name in roles:
                    role_class = apps.get_model("data", role_name)
                    role_class.objects.get_or_create(company=company, user=recipient)

                try:
                    email.send_sib_template(
                        email.EmailTemplateID.USER_ADDED_TO_COMPANY.value,
                        {
                            "SENDER_NAME": sender.get_full_name(),
                            "COMPANY_NAME": company.social_name,
                            "DASHBOARD_LINK": f"{get_base_url()}tableau-de-bord?company={company.id}",
                        },
                        recipient.email,
                        recipient.get_full_name(),
                    )
                except Exception as e:
                    logger.error(f"Email not sent on AddNewCollaboratorView for recipient {recipient.id}")
                    logger.exception(e)

                return Response({"message": f"{recipient.name} a été ajouté à vos collaborateurs."})
