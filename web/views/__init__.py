from django.views.generic import TemplateView
from .user import RegisterUserView, ProConnectBackend
from .certificate import CertificateView
from .summary import SummaryView


class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue-app.html"
