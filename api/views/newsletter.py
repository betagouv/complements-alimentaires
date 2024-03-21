import logging
import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..utils.responses import EmptyValidResponse
import sib_api_v3_sdk
from django.contrib.auth import get_user_model


User = get_user_model()

logger = logging.getLogger(__name__)


class SubscribeNewsletter(APIView):
    def post(self, request):
        email = request.data["email"].strip()
        User.objects.normalize_email(email)
        validate_email(email)

        list_id = settings.NEWSLETTER_BREVO_LIST_ID
        if not list_id:
            raise ImproperlyConfigured("NEWSLETTER_BREVO_LIST_ID setting should be set")

        try:
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key["api-key"] = settings.ANYMAIL.get("SENDINBLUE_API_KEY")
            api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
            create_contact = sib_api_v3_sdk.CreateContact(email=email)
            create_contact.list_ids = [list_id]
            create_contact.update_enabled = True
            api_instance.create_contact(create_contact)
            return EmptyValidResponse
        except sib_api_v3_sdk.rest.ApiException as e:
            if json.loads(e.body).get("message") == "Contact already exist":
                return Response("Cette adresse e-mail est déjà inscrite à notre newsletter", status=status.HTTP_200_OK)
            raise e
