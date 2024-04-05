from django.conf import settings


def get_base_url() -> str:
    scheme = "https" if settings.SECURE else "http"
    return f"{scheme}://{settings.HOSTNAME}/"
