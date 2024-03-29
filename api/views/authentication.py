from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from api.exceptions import ProjectAPIException


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_verified:
                raise ProjectAPIException(
                    non_field_errors=[
                        "Votre compte n'est pas encore vérifié. Veuillez vérifier vos e-mails reçus, et vos courriers indésirables."
                    ],
                    extra={"user_id": user.id},
                )
            login(request, user)  # will create the user session
            return Response({"csrf_token": get_token(request)})
        else:
            raise ProjectAPIException(
                non_field_errors=["Ce couple identifiant/mot de passe ne permet pas de vous identifier."]
            )


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response()
