from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token

from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers
from urllib.parse import urlencode

# from django.conf import settings
# from django.shortcuts import resolve_url
# from django.urls import reverse
# from django.utils import crypto
# from django.utils.module_loading import import_string
# import urllib

from rest_framework.response import Response
from rest_framework.views import APIView
from mozilla_django_oidc.utils import absolutify, import_from_settings
from mozilla_django_oidc.views import OIDCLogoutView

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
    # # # from https://github.com/mozilla/mozilla-django-oidc/blob/86660c22c842d935551e3da7ab14709e53facd12/mozilla_django_oidc/views.py#L256
    # def oidc_logout(self, request):
    #     logout_url = settings.LOGOUT_REDIRECT_URL

    #     if request.user.is_authenticated:
    #         logout_endpoint = settings.OIDC_OP_LOGOUT_ENDPOINT
    #         id_token = request.session.get('oidc_id_token')
    #         state = "randomly-generated-string"
    #         logout_redirect = "http://127.0.0.1:8000/platform/oidc/logout/"
    #         # logout_redirect = "http://127.0.0.1:5173/entreprises"
    #         logout_redirect = urllib.parse.quote_plus(logout_redirect)
    #         logout_url = f"{logout_endpoint}?id_token={id_token}&state={state}&post_logout_redirect_uri={logout_redirect}"
    #         print(logout_url)
    #         # print(logout_url)
    #         # logout_from_op = settings.OIDC_OP_LOGOUT_URL_METHOD
    #         # if logout_from_op:
    #         #     logout_url = import_string(logout_from_op)(request)
    #         # logout(request)
    #     return HttpResponseRedirect(logout_url)

    # inspired by https://github.com/suitenumerique/django-lasuite/blob/7dc91fd69bd8dc58d1599bcdb74f30fc7d73c200/src/lasuite/oidc_login/views.py#L48
    # Template of the auto-submitted form
    logout_form_template_name = "oidc_login/logout_form.html"

    @staticmethod
    def get_settings(attr, *args):
        """Retrieve a parameter from Django settings."""
        return import_from_settings(attr, *args)

    @staticmethod
    def persist_state(request, state):
        """
        Persist the given 'state' parameter in the session's 'oidc_states' dictionary.

        This method is used to store the OIDC state parameter in the session, according to the
        structure expected by Mozilla Django OIDC's 'add_state_and_verifier_and_nonce_to_session'
        utility function.
        """
        if "oidc_states" not in request.session or not isinstance(request.session["oidc_states"], dict):
            request.session["oidc_states"] = {}

        request.session["oidc_states"][state] = {}

        # Force immediate session save for cache-based backends
        request.session.modified = True
        request.session.save()

    def get_oidc_logout_request(self, request):
        """
        Build the logout request to send to the OIDC provider.

        Retrieves the necessary parameters from the session and returns a
        `(logout_endpoint, parameters)` tuple.

        If no logout endpoint is configured or no ID token is found in the session,
        the logout flow will not be initiated, and the method will return None.

        The 'state' parameter is generated randomly and persisted in the session to ensure
        its integrity during the subsequent callback.
        """
        oidc_logout_endpoint = self.get_settings("OIDC_OP_LOGOUT_ENDPOINT")

        if not oidc_logout_endpoint:
            return None

        reverse_url = "http://127.0.0.1:5173/"  # reverse("api:oidc_logout_callback")
        id_token = request.session.get("oidc_id_token", None)

        if not id_token:
            return None

        parameters = {
            # "id_token_hint": id_token,
            "client_id": self.get_settings("OIDC_RP_CLIENT_ID"),
            # "state": crypto.get_random_string(self.get_settings("OIDC_STATE_SIZE", 32)),
            "post_logout_redirect_uri": absolutify(request, reverse_url),
        }

        # self.persist_state(request, parameters["state"])

        return oidc_logout_endpoint, parameters

    def construct_oidc_logout_response(self, request):
        """
        Create the response sending the user to the OIDC provider to start the logout process.

        According to the OpenID Connect RP-Initiated Logout specification, the logout request
        goes through the user agent for the OIDC provider to end its own session, using:
        # - the HTTP GET method (default): redirects to the OIDC logout endpoint, the parameters
        #   being serialized in the URL query string;
        - the HTTP POST method: returns an
          auto-submitted HTML form, the parameters being serialized using Form Serialization.

        If the logout flow cannot be initiated, the method will return None.
        """
        logout_request = self.get_oidc_logout_request(request)

        print("logout_request", logout_request)
        if logout_request is None:
            return None

        oidc_logout_endpoint, parameters = logout_request

        if not self.get_settings("OIDC_OP_LOGOUT_USE_POST", False):
            print("redirecting without post")
            return HttpResponseRedirect(f"{oidc_logout_endpoint}?{urlencode(parameters)}")

        response = TemplateResponse(
            request,
            self.logout_form_template_name,
            {
                "oidc_logout_endpoint": oidc_logout_endpoint,
                "parameters": parameters,
                # Set by django-csp, to allow the auto-submit inline script
                # "csp_nonce": getattr(request, "csp_nonce", None),
            },
        )
        print(request.session)
        print(request.session.get("id"))
        response.set_cookie(key="sessionid", value=request.session.session_key, samesite="None", secure=True)
        # response.cookies['sessionid']['samesite'] = 'None'
        # response.cookies['sessionid']['secure'] = True
        # The page contains the ID token, it must never be cached
        add_never_cache_headers(response)
        return response

    def post(self, request, *args, **kwargs):
        logout_response = None
        oidc_id_token = request.session.get("oidc_id_token")
        print("oidc_id_token", oidc_id_token)
        if oidc_id_token:
            logout_response = self.construct_oidc_logout_response(request)
        if logout_response is None:
            logout(request)
            return Response()

        # Force final session save before sending the user to SSO
        # This ensures the logout state generated in get_oidc_logout_request()
        # is persisted in Redis before the browser leaves
        request.session.modified = True
        request.session.save()
        print(logout_response)
        return logout_response


# def oidc_logout(request):
#     print("oidc logout")
#     logout_endpoint = settings.OIDC_OP_LOGOUT_ENDPOINT
#     id_token = request.session.get('oidc_id_token')
#     state = request.session.get('oidc_state')
#     redirect_url = f"{logout_endpoint}?id_token={id_token}&state={state}&post_logout_redirect_uri={settings.LOGOUT_REDIRECT_URL}"
#     return redirect_url

# class OIDCLogoutView(APIView):
#     def get(self, request):
#         print("hi")
#         return Response()


class OIDCLogoutCallbackView(OIDCLogoutView):
    """
    Custom view for handling the logout callback from the OpenID Connect (OIDC) provider.

    Handles the callback after logout from the identity provider (OP).
    Verifies the state parameter and performs necessary logout actions.

    The Django session is maintained during the logout process to ensure the integrity
    of the logout flow initiated in the previous step.
    """

    http_method_names = ["get"]

    def get(self, request):
        """
        Handle the logout callback.

        If the user is not authenticated, redirects to the default logout URL.
        Otherwise, verifies the state parameter and performs necessary logout actions.
        """
        print("logout callback", request.user.is_authenticated)
        if not request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_url)

        state = request.GET.get("state")

        # Handle requests without state parameter
        # Some SSO providers send a preflight request without state before the actual callback
        # We should not raise an error in this case, just redirect gracefully
        if not state:
            return HttpResponseRedirect(self.redirect_url)

        # if state not in request.session.get("oidc_states", {}):
        #     msg = "OIDC callback state not found in session `oidc_states`!"
        #     raise SuspiciousOperation(msg)

        # Clean up the state from session
        del request.session["oidc_states"][state]
        request.session.save()

        # Perform Django logout
        logout(request)

        return HttpResponseRedirect(self.redirect_url)
