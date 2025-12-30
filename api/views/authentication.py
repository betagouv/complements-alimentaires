from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db.models import Q
from django.middleware.csrf import get_token

from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import ProjectAPIException


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get("username")
        password = request.data.get("password")

        incomplete_data_msg = "Veuillez fournir un identifiant et un mot de passe."
        unauthorized_msg = "Ce couple identifiant/mot de passe ne permet pas de vous identifier."
        unverified_msg = "Votre compte n'est pas encore vérifié. Veuillez vérifier vos e-mails reçus, et vos courriers indésirables."

        if not username_or_email or not password:
            raise ProjectAPIException(non_field_errors=[incomplete_data_msg])

        try:
            user = get_user_model().objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except get_user_model().DoesNotExist:
            raise ProjectAPIException(non_field_errors=[unauthorized_msg])

        authenticated_user = authenticate(request, username=user.username, password=password)
        if not authenticated_user:
            raise ProjectAPIException(non_field_errors=[unauthorized_msg])

        if not authenticated_user.is_verified:
            raise ProjectAPIException(non_field_errors=[unverified_msg], extra={"user_id": authenticated_user.id})

        login(request, authenticated_user)  # will create the user session
        return Response({"csrf_token": get_token(request)})


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response()
