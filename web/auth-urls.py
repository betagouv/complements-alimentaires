from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
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
]
