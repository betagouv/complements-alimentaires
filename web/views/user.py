from django.views.generic import FormView
from django.http import HttpResponseRedirect
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
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


class ProConnectBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super().create_user(claims)

        print(user.__class__)
        print(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("usual_name", "")
        # TODO: uid/sub, siret, roles ?
        user.save()

        return user
