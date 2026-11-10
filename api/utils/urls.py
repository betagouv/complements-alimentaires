from django.conf import settings


def get_base_url() -> str:
    scheme = "https" if settings.SECURE else "http"
    return f"{scheme}://{settings.HOSTNAME}/"


def get_admin_url() -> str:
    return f"{get_base_url()}platform/{settings.ADMIN_URL}/"
