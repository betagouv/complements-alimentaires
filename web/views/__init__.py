from django.views.generic import TemplateView

from .file_upload import FileUploadView
from .user import RegisterUserView


class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue-app.html"
