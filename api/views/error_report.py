import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.defaultfilters import date, time
from django.utils import timezone

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from api.serializers import ErrorReportSerializer
from data.models import ErrorReport

logger = logging.getLogger(__name__)


class ErrorReportCreateView(CreateAPIView):
    model = ErrorReport
    permission_classes = [AllowAny]
    serializer_class = ErrorReportSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()
        self.send_email(serializer.instance)

    def send_email(self, error_report):
        try:
            now = timezone.now()
            author = error_report.author
            author_str = error_report.email or (
                f"{author.name} ({author.email})" if author else "Un utilisateur anonyme"
            )

            send_mail(
                subject="Nouvelle incohérence remontée dans la base ingrédients",
                message=f"{author_str} a envoyé un message le {date(now)} à {time(now)} pour signaler l'erreur suivante concernant l'ingrédient {error_report.element_string} : {error_report.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
            )
        except Exception as e:
            logger.exception(e)
