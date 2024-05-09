from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models import CollaborationInvitation, Company, CoSupervisionClaim

from ..exception_handling import ProjectAPIException
from ..permissions import IsSolicitationRecipient
from ..serializers import CoSupervisionClaimSerializer

User = get_user_model()


class CoSupervisionClaimListView(ListAPIView):
    serializer_class = CoSupervisionClaimSerializer

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company.objects.filter(supervisors=user), pk=self.kwargs["pk"])
        return CoSupervisionClaim.objects.filter(recipients=user, company=company, processor__isnull=True)


class ProcessCoSupervisionClaim(APIView):
    """Effectue une action de traitement sur une demande de co-gestion"""

    permission_classes = [IsSolicitationRecipient]

    def post(self, request, pk: int, *args, **kwargs):
        solicitation = get_object_or_404(CoSupervisionClaim, pk=pk)
        self.check_object_permissions(request, solicitation)
        action = getattr(solicitation, request.data["action_name"])
        action(processor=request.user)
        return Response({})


class CollaborationInvitationCreateView(APIView):
    # TODO: transformer en APIView ?

    @transaction.atomic
    def post(self, request, pk: int, *args, **kwargs):
        company = get_object_or_404(Company, pk=pk)
        cleaned_email = User.objects.normalize_email(request.data["recipient_email"])
        sender = request.user
        try:
            recipient = User.objects.get(email=cleaned_email)
        except User.DoesNotExist:
            # Cas A : l'utilisateur n'existe pas en base, mais une invitation non traitée a déjà été envoyée
            if CollaborationInvitation.objects.filter(
                sender=sender, company=company, recipient_email=cleaned_email, processed_at__isnull=True
            ).exists():
                raise ProjectAPIException(global_error="Une invitation a déjà été envoyée pour cette adresse e-mail.")
            # Cas B : l'utilisateur n'existe pas en base, et aucune invitation n'a été envoyée
            CollaborationInvitation.objects.create(
                sender=sender, company=company, recipient_email=cleaned_email, roles=request.data["roles"]
            )
            return Response({"message": f"L'invitation a bien été envoyéee à {cleaned_email}."})
        else:
            # Cas C : l'utilisateur existe en base et fait déjà partie des collaborateurs de l'entreprise
            if recipient in company.collaborators:
                raise ProjectAPIException(
                    field_errors={"recipient_email": "Cet utilisateur fait déjà partie de vos collaborateurs."}
                )
            # Cas D : l'utilisateur existe en base mais n'est pas encore collaborateur de l'entreprise
            else:
                for role_name in request.data["roles"]:
                    role_class = apps.get_model("data", role_name)
                    role_class.objects.get_or_create(
                        company=company, user=recipient
                    )  # le get évite une potentielle erreur

                send_mail(
                    subject=f"[Compl'Alim] {sender.name} vous a ajouté en tant que collaborateur.",
                    message=f"{sender.name} vous a ajouté en tant que collaborateur de l'entreprise {company.social_name}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[sender.email],
                )
                return Response(
                    {
                        "message": f"{recipient.name} a été ajouté à vos collaborateurs. Un e-mail a été envoyé pour le prévenir."
                    }
                )
