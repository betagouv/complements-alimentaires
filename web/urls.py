from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from web.views import VueAppDisplayView, RegisterUserView, FileUploadView

urlpatterns = [
    path("", VueAppDisplayView.as_view(), name="app"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.LoginView
    path(
        "s-identifier",
        auth_views.LoginView.as_view(
            template_name="auth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.LogoutView
    path(
        "se-deconnecter",
        auth_views.LogoutView.as_view(
            template_name="auth/logged_out.html",
        ),
        name="logout",
    ),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.PasswordChangeView
    path(
        "modification-mot-de-passe",
        auth_views.PasswordChangeView.as_view(
            template_name="auth/password_change_form.html",
        ),
        name="password_change",
    ),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.PasswordChangeDoneView
    path(
        "mot-de-passe-modifie",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="auth/password_change_done.html",
        ),
        name="password_change_done",
    ),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.PasswordResetView
    path(
        "reinitialisation-mot-de-passe",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset_form.html",
        ),
        name="password_reset",
    ),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.PasswordResetDoneView
    path(
        "email-reinitialisation-envoye",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.PasswordResetConfirmView
    path(
        "nouveau-mot-de-passe/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.views.PasswordResetCompleteView
    path(
        "mot-de-passe-reinitialise",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("creer-mon-compte", RegisterUserView.as_view(), name="register"),
    path("envoyer-un-fichier", FileUploadView.as_view(), name="file_upload"),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
