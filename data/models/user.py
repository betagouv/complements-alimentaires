from functools import cached_property
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from data.mixins import AutoValidable, Deactivable
from django.db.models import OneToOneRel
from django.core.exceptions import ObjectDoesNotExist
from .roles import BaseRole


class User(AutoValidable, Deactivable, AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    class Meta:
        verbose_name = "utilisateur"
        ordering = ["-date_joined"]
        get_latest_by = "date_joined"

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
    ]

    def clean(self) -> None:
        # NOTE: full_clean() is called in save() with the Autovalidable mixin
        super().clean()
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.upper()

    @cached_property
    def roles(self) -> list[BaseRole]:
        """Get the 0 -> N roles object from the user"""
        roles = []
        for f in User._meta.get_fields():
            if isinstance(f, OneToOneRel) and issubclass(f.related_model, BaseRole):
                try:
                    roles.append(getattr(self, f.name))
                except ObjectDoesNotExist:
                    pass
        return roles

    @cached_property
    def role(self, name) -> BaseRole | None:
        """Get the given role or None if it does not exist."""
        try:
            return getattr(self, name)
        except ObjectDoesNotExist:
            return None

    @property
    def name(self) -> str:
        """Syntaxic sugar"""
        return self.get_full_name()

    def __str__(self):
        return self.name
