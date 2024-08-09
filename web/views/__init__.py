from django.views.generic import TemplateView
from .user import RegisterUserView
from .file_upload import FileUploadView
from .certificate import CertificateView


class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue-app.html"
