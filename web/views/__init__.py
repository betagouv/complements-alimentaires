from django.views.generic import TemplateView
from .user import RegisterUserView
from .file_upload import FileUploadView
from .pdf_generator import generate_pdf


class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue-app.html"
