import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3 import S3Storage


class FileUploadMixin:
    location = os.path.join(settings.MEDIA_ROOT, "uploads")
    base_url = urljoin(settings.MEDIA_URL, "uploads/")


class FileUploadS3Storage(FileUploadMixin, S3Storage):
    """Custom storage for django_ckeditor_5 images, located on S3"""


class FileUploadFileSystemStorage(FileUploadMixin, FileSystemStorage):
    """Custom storage for django_ckeditor_5 images, located on file system"""
