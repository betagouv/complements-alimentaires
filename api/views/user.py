import logging
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.db import transaction
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exception_handling import ProjectAPIException
from api.permissions import CanAccessUser, IsController
from api.serializers import (
    ChangePasswordSerializer,
    CreateUserSerializer,
    UserSerializer,
)
from config import email
from data.models.solicitation import CollaborationInvitation
from tokens.models import MagicLinkToken, MagicLinkUsage

from ..utils.urls import get_base_url

User = get_user_model()
logger = logging.getLogger(__name__)


def _send_verification_mail(user):
    new_token = MagicLinkToken.objects.create(user=user, usage=MagicLinkUsage.VERIFY_EMAIL_ADDRESS)
    verification_url = urljoin(get_base_url(), new_token.as_url(key=new_token.key))
    brevo_template_id = 19
    try:
        email.send_sib_template(
            brevo_template_id,
            {"CONFIRMATION_LINK": verification_url},
            user.email,
            user.get_full_name(),
        )
    except Exception as e:
        logger.error(f"Email verification email not sent on _send_verification_mail for recipient {user.email}")
        logger.exception(e)


class LoggedUserView(APIView):
    def get(self, request, *args, **kwargs):
        """Retourne les données d'un utilisateur connecté"""

        user = request.user
        if user.is_active:
            return Response(UserSerializer(user).data)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserCreateView(CreateAPIView):
    """Inscription d'un utilisateur connecté"""

    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        new_user = serializer.save()
        # ajout automatique de rôles collaborateurs, si des invitations liées existent
        for solicitation in CollaborationInvitation.objects.filter(
            recipient_email=new_user.email, processed_at__isnull=True
        ):
            solicitation.account_created(processor=new_user)
        _send_verification_mail(new_user)
        return new_user


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    - Modification d'un utilisateur connecté (hors mot de passe)
    - Désactivation d'un utilisateur
    - Obtention d'un utilisateur (aujourd'hui principalement par le rôle instructor)
    """

    permission_classes = [IsAuthenticated, CanAccessUser]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.active()

    @transaction.atomic
    def perform_update(self, serializer):
        user = serializer.instance
        old_email = user.email
        serializer.save()
        if user.email != old_email:
            user.unverify()
            _send_verification_mail(user)

    def perform_destroy(self, user):
        user.deactivate()
        send_mail(
            subject="Nouvelle demande de suppression de compte",
            message=f"{user.name} (id: {user.id}) a demandé la suppression de son compte.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )


class UserRetrieveControlView(RetrieveAPIView):
    permission_classes = [IsController]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.active()


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({}, status=status.HTTP_200_OK)


class SendNewSignupVerificationEmailView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        _send_verification_mail(user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GenerateUsernameView(APIView):
    def get(self, request, *args, **kwargs):
        first_name = request.query_params.get("first_name")
        last_name = request.query_params.get("last_name")
        if not first_name or not last_name:
            raise ProjectAPIException(global_error="Les champs nom et prénom doivent être remplis.")
        return Response({"username": User.generate_username(first_name, last_name)})


class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        key = request.data.get("key")
        if not key:
            raise ProjectAPIException(global_error="Lien de validation invalide.")
        user = MagicLinkToken.run_email_verification(key)
        if user:
            # we log the user in to avoid an unnecessary login step
            login(request, user)  # will create the user session
            return Response({"csrf_token": get_token(request)})
        else:
            raise ProjectAPIException(
                global_error="Le lien de validation n'a pas fonctionné. Il a peut-être été déjà utilisé ou n'est plus valide."
            )
