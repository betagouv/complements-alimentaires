from urllib.parse import urlencode

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils import crypto
from django.views import View

from mozilla_django_oidc.utils import absolutify, import_from_settings
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

        login(request, authenticated_user)  # crée la session utilisateur
        return Response({"csrf_token": get_token(request)})


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.session.get("oidc_id_token"):
            logout_url = self.get_oidc_logout_url(request)
            if logout_url:
                # La session doit rester active pour que le callback puisse vérifier le state.
                # La déconnexion Django a lieu dans OIDCLogoutCallbackView.
                request.session.modified = True
                request.session.save()
                return Response({"logout_url": logout_url})

        logout(request)
        return Response({})

    @staticmethod
    def get_settings(attr, *args):
        return import_from_settings(attr, *args)

    @staticmethod
    def persist_state(request, state):
        if "oidc_states" not in request.session or not isinstance(request.session["oidc_states"], dict):
            request.session["oidc_states"] = {}
        request.session["oidc_states"][state] = {}
        request.session.modified = True
        request.session.save()

    def get_oidc_logout_url(self, request):
        """
        Construit et retourne l'URL de déconnexion du fournisseur OIDC, ou None si la déconnexion OIDC ne peut pas être initiée.

        Nécessite un endpoint de déconnexion configuré et un id_token en session.
        Génère un state aléatoire pour la protection CSRF et le persiste en session pour que le callback puisse le vérifier.
        """
        oidc_logout_endpoint = self.get_settings("OIDC_OP_LOGOUT_ENDPOINT", "")
        if not oidc_logout_endpoint:
            return None

        id_token = request.session.get("oidc_id_token")
        if not id_token:
            return None

        state = crypto.get_random_string(32)
        self.persist_state(request, state)

        callback_url = absolutify(request, reverse("api:oidc_logout_callback"))
        parameters = {
            "id_token_hint": id_token,
            "client_id": self.get_settings("OIDC_RP_CLIENT_ID"),
            "state": state,
            "post_logout_redirect_uri": callback_url,
        }

        return f"{oidc_logout_endpoint}?{urlencode(parameters)}"


class OIDCLogoutCallbackView(View):
    """Gère le retour du fournisseur OIDC après la fin de la session SSO."""

    @property
    def redirect_url(self):
        return import_from_settings("LOGOUT_REDIRECT_URL", "/")

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_url)

        state = request.GET.get("state")
        if not state:
            return HttpResponseRedirect(self.redirect_url)

        oidc_states = request.session.get("oidc_states", {})
        if state not in oidc_states:
            raise SuspiciousOperation("OIDC logout callback state not found in session")

        oidc_states.pop(state)
        request.session["oidc_states"] = oidc_states
        request.session.save()

        logout(request)
        return HttpResponseRedirect(self.redirect_url)
