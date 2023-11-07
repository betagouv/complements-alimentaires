from django.shortcuts import render
from django.views.generic import TemplateView

class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """
    template_name = "vue-app.html"
