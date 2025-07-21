import os
from urllib.parse import urljoin

from django.conf import settings


class FileUploadMixin:
    location = os.path.join(settings.MEDIA_ROOT, "uploads")
    base_url = urljoin(settings.MEDIA_URL, "uploads/")
