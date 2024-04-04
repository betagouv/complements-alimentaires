from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.db import transaction
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exception_handling import ProjectAPIException
from api.serializers import (
    ChangePasswordSerializer,
    CreateUserSerializer,
    EditUserSerializer,
    LoggedUserSerializer,
)
from tokens.models import MagicLinkToken, MagicLinkUsage

from ..utils.urls import get_base_url

User = get_user_model()


def _send_verification_mail(user):
    new_token = MagicLinkToken.objects.create(user=user, usage=MagicLinkUsage.VERIFY_EMAIL_ADDRESS)
    verification_url = urljoin(get_base_url(), new_token.as_url(key=new_token.key))
    send_mail(
        subject="Vérifiez votre adresse e-mail",
        message=f"Cliquez sur le lien suivant pour vérifier votre adresse e-mail : {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


class UserView(APIView):
    """La gestion d'utilisateur, particulièrement adaptée à l'architecture REST"""

    def get_permissions(self):
        return [AllowAny()] if self.request.method in ["GET", "POST"] else [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        """Retourne les données d'un utilisateur connecté"""

        user = request.user
        if user.is_active:
            return Response(LoggedUserSerializer(user).data)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        """Créé un utilisateur (inscription)"""

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            _send_verification_mail(new_user)
            return Response({"user_id": new_user.id}, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """Modifie le profil d'un utilisateur (hors changement de mot de passe)"""

        user = request.user
        old_email = user.email
        serializer = EditUserSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if user.email != old_email:
                user.unverify()
                _send_verification_mail(user)
            return Response(LoggedUserSerializer(user).data)

    def delete(self, request, *args, **kwargs):
        """Désactive l'utilisateur, sans le supprimer en base"""

        user = request.user
        user.deactivate()
        send_mail(
            subject="Nouvelle demande de suppression de compte",
            message=f"{user.name} (id: {user.id}) a demandé la suppression de son compte.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return Response({}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({}, status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """NOTE: this does not delete anything actually"""
        user = request.user
        user.deactivate()
        send_mail(
            subject="Nouvelle demande de suppression de compte",
            message=f"{user.name} (id: {user.id}) a demandé la suppression de son compte.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return Response({})


class SendNewSignupVerificationEmailView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        _send_verification_mail(user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GenerateUsernameView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"username": User.generate_username(**request.query_params)})


class VerifyEmailView(APIView):
    def post(self, request, *args, **kwargs):
        user = MagicLinkToken.run_email_verification(request.data["key"])
        if user:
            # we log the user in to avoid an unnecessary login step
            login(request, user)  # will create the user session
            return Response({"csrf_token": get_token(request)})
        else:
            raise ProjectAPIException(
                global_error="Le lien de validation n'a pas fonctionné. Il a peut-être été déjà utilisé ou n'est plus valide."
            )
