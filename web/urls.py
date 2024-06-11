from django.urls import path
from django.views.generic.base import TemplateView

from web.views import FileUploadView, VueAppDisplayView, generate_pdf

urlpatterns = [
    path("", VueAppDisplayView.as_view(), name="app"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("pdf", generate_pdf, name="pdf_generator"),
    path("envoyer-un-fichier", FileUploadView.as_view(), name="file_upload"),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
