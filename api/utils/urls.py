from django.http import HttpRequest


def get_base_url(request: HttpRequest) -> str:
    return f"{request.scheme}://{request.get_host()}/"
