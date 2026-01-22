import logging
import os
from abc import ABC, abstractmethod

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from rest_framework.generics import GenericAPIView
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)


class PdfView(GenericAPIView, ABC):
    as_html = False

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if self.as_html:
            return render(request, self.get_template_path(obj), self.get_context(obj))

        template = get_template(self.get_template_path(obj))
        html = template.render(self.get_context(obj))
        response = HttpResponse(content_type="application/pdf")
        filename = self.get_pdf_file_name(obj)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=PdfView.link_callback)

        if pisa_status.err:
            logger.error(f"Error while generating PDF for {obj.__class__.__name__} {obj.id}:\n{pisa_status.err}")
            return HttpResponse("An error ocurred", status=500)

        return response

    @staticmethod
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources.
        """
        # Gestion des fichiers STATIC
        if uri.startswith(settings.STATIC_URL):
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        # Gestion des fichiers MEDIA
        elif uri.startswith(settings.MEDIA_URL):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        else:
            return uri  # On le laisse tel qu'il est car pas static ni media

        return path

    @abstractmethod
    def get_context(self, obj):
        pass

    @abstractmethod
    def get_pdf_file_name(self, obj):
        pass

    @abstractmethod
    def get_template_path(self, obj):
        pass
