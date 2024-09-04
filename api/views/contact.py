import logging

from django.conf import settings
from django.core.mail import EmailMessage

from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import ProjectAPIException

logger = logging.getLogger(__name__)


class ContactView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email", "").strip()
            name = request.data.get("name")
            message = request.data.get("message")

            if not email or not name or not message:
                logger.error(f"Missing field from contact view. Name: {name}, email: {email}, message: {message}.")
                raise ProjectAPIException(non_field_errors=["Merci de remplir tous les champs obligatoires."])

            subject = f"Demande de support de {name}"

            body = f"Nom/Prénom\n{name}\n------"
            body += f"\n\nAdresse email\n{email}\n------"
            body += f"\n\nMessage\n« {message} »\n------"

            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[email],
            )
            email.send()
            return Response()
        except Exception as e:
            logger.exception(f"Exception ocurred while handling contact request. {e}")
            raise ProjectAPIException(
                non_field_errors=[
                    "Une erreur est survenu lors de l'envoi de votre message. Merci de réessayer ultérieurement."
                ]
            )
