from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
