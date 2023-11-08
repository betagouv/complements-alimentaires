from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, FormView

class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """
    template_name = "vue-app.html"

class RegisterUserView(FormView):
    """
    View containing the user-only form to create an account
    """

    form_class = UserCreationForm
    template_name = "auth/register.html"
