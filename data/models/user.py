from functools import cached_property
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db import models, transaction
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from data.behaviours import AutoValidable, Deactivable, DeactivableQuerySet
from django.db.models import OneToOneRel
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .roles import BaseRole


class UserQuerySet(DeactivableQuerySet):
    pass


class UserManager(BaseUserManager):
    @transaction.atomic()
    def create_user(self, email, password=None, **extra_fields):
        """Custom User Manager is required when defining a custom User class"""

        user = self.model(
            email=email,
            is_superuser=False,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_verified = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AutoValidable, Deactivable, AbstractBaseUser):
    class Meta:
        verbose_name = "utilisateur"
        ordering = ["-date_joined"]
        get_latest_by = "date_joined"

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField("numéro de téléphone", blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_verified = models.BooleanField("Compte vérifié ?", default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager.from_queryset(UserQuerySet)()

    def clean(self) -> None:
        # NOTE: full_clean() is called in save() with the Autovalidable mixin
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()

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

    def get_full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    @classmethod
    def generate_username(cls, first_name, last_name) -> str:
        """Return an auto-generated username that could be valid based on given user infos
        ⛔️ Using `while...True` structure must be tested carefully to avoid infinite loop.
        """

        assert all([first_name, last_name])  # given fields can't be empty
        base_username = slugify(first_name) + "." + slugify(last_name)
        i = 1
        while "the generated username already exists in database":
            suffix = "" if i == 1 else str(i)
            username = base_username + suffix
            if not cls.objects.filter(username=username).exists():
                return username
            i += 1

    def verify(self):
        """Mark an account as verified."""
        self.is_verified = True
        self.save()

    @property
    def name(self) -> str:
        """Syntaxic sugar"""
        return self.get_full_name()

    def __str__(self):
        return self.name
