from django.conf import settings


class SecureFileServingMiddleware:
    """
    Ajout du header de sécurité sur les fichiers servis depuis MEDIA_URL
    pour éviter l'exécution de XSS dans les fichiers téléversés.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.MEDIA_URL and request.path.startswith(settings.MEDIA_URL):
            response["Content-Disposition"] = "attachment"
        return response
