from django.urls import path
from django.views.generic.base import TemplateView

from web.views import CertificateView, FileUploadView, SummaryView, VueAppDisplayView

urlpatterns = [
    path("", VueAppDisplayView.as_view(), name="app"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.LoginView
    path("envoyer-un-fichier", FileUploadView.as_view(), name="file_upload"),
    path("declarations/<int:pk>/certificate", CertificateView.as_view(), name="certificate"),
    path("declarations/<int:pk>/summary", SummaryView.as_view(), name="summary"),
    # html view primarily used for development purposes
    path("declarations/<int:pk>/summary-html", SummaryView.as_view(as_html=True), name="summary_html"),
]
