from django.views.generic import FormView
from django.http import HttpResponseRedirect
from ..forms import RegisterUserForm


class RegisterUserView(FormView):
    """
    View containing the user-only form to create an account
    """

    form_class = RegisterUserForm
    template_name = "auth/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get("next", "/")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
