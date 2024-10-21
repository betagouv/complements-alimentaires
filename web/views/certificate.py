import logging
import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template

from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from xhtml2pdf import pisa

from api.permissions import CanAccessIndividualDeclaration
from data.models import Declaration

logger = logging.getLogger(__name__)


class CertificateView(GenericAPIView):
    permission_classes = [CanAccessIndividualDeclaration]
    queryset = Declaration.objects.all()

    def get(self, request, *args, **kwargs):
        declaration = self.get_object()
        template = get_template(self.get_template_path(declaration))
        html = template.render(self.get_context(declaration))

        response = HttpResponse(content_type="application/pdf")
        filename = self.get_pdf_file_name(declaration)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=CertificateView.link_callback)

        if pisa_status.err:
            logger.error(f"Error while generating PDF for teledeclaration {declaration.id}:\n{pisa_status.err}")
            return HttpResponse("An error ocurred", status=500)

        return response

    def get_template_path(self, declaration):
        status = Declaration.DeclarationStatus
        article_map = {
            Declaration.Article.ARTICLE_15: 15,
            Declaration.Article.ARTICLE_15_WARNING: 15,
            Declaration.Article.ARTICLE_16: 16,
        }
        article = article_map.get(declaration.article, 15)
        if declaration.status in [
            status.AWAITING_INSTRUCTION,
            status.AWAITING_VISA,
            status.ONGOING_INSTRUCTION,
            status.ONGOING_VISA,
        ]:
            return f"certificates/certificate-submitted-art-{article}.html"
        if declaration.status in [status.AUTHORIZED, status.WITHDRAWN]:
            return f"certificates/certificate-art-{article}.html"
        if declaration.status == status.REJECTED:
            return "certificates/certificate-rejected.html"

        raise NotFound()

    def get_context(self, declaration):
        status = Declaration.DeclarationStatus
        date_statuses = [status.AWAITING_INSTRUCTION, status.AUTHORIZED, status.REJECTED]

        try:
            date = declaration.snapshots.filter(status__in=date_statuses).latest("creation_date").creation_date
        except Exception as e:
            logger.error(f"Error obtaining certificate date for declaration {declaration.id}")
            logger.exception(e)
            date = declaration.creation_date

        try:
            last_submission_date = (
                declaration.snapshots.filter(status=status.AWAITING_INSTRUCTION).latest("creation_date").creation_date
            )
        except Exception as e:
            logger.error(f"Error obtaining last submission date for declaration {declaration.id}")
            logger.exception(e)
            last_submission_date = declaration.creation_date

        return {
            "date": date,
            "last_submission_date": last_submission_date,
            "include_recipient_address": declaration.status == Declaration.DeclarationStatus.REJECTED,
            "recipient_lines": [
                declaration.company.social_name,
                declaration.company.address,
                f"{declaration.company.city} {declaration.company.country}",
            ],
            "declaration": declaration,
        }

    def get_pdf_file_name(self, declaration):
        return f"attestation-{declaration.name}.pdf"

    @staticmethod
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        https://xhtml2pdf.readthedocs.io/en/latest/usage.html#using-xhtml2pdf-in-django
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL
            sRoot = settings.STATIC_ROOT
            mUrl = settings.MEDIA_URL
            mRoot = settings.MEDIA_ROOT

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception("media URI must start with {} or {}".format(sUrl, mUrl))
        return path
