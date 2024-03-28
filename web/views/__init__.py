from django.views.generic import TemplateView
from .user import RegisterUserView  # noqa: F401
from .file_upload import FileUploadView  # noqa: F401


class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue-app.html"
