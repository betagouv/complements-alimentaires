import logging
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import date, time
from ..utils.emails import get_email_from_request
from ..utils.responses import EmptyValidResponse
from api.exceptions import InvalidEmail


logger = logging.getLogger(__name__)


class ReportIssue(APIView):
    def post(self, request):
        try:
            email = get_email_from_request(request, required=False)
        except ValidationError:  # NOTE: should not actually happen with the front-end validation
            raise InvalidEmail
        now = timezone.now()
        user_str = email or "Un utilisateur anonyme"
        element_str = request.data["element_name"]
        message_str = request.data["report_message"]
        time_str = f"le {date(now)} à {time(now)}"

        send_mail(
            subject="Nouvelle incohérence remontée dans la base ingrédients",
            message=f"{user_str} a envoyé un message {time_str} pour signaler l'erreur suivante concernant l'ingrédient {element_str} : {message_str}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )

        return EmptyValidResponse
