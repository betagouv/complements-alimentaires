from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.fields import ObjectDoesNotExist

from data.behaviours import AutoValidable, Deactivable, DeactivableQuerySet, Verifiable

from .company import CompanyRole
from .global_roles import BaseGlobalRole


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


class User(PermissionsMixin, AutoValidable, Verifiable, Deactivable, AbstractBaseUser):
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

    def get_global_roles(self) -> list[BaseGlobalRole]:
        """Récupère les rôles globaux directement liés à cet utilisateur"""
        roles = []
        for f in User._meta.get_fields():
            if isinstance(f, models.OneToOneRel) and issubclass(f.related_model, BaseGlobalRole):
                try:
                    roles.append(getattr(self, f.name))
                except ObjectDoesNotExist:
                    pass
        return roles

    def get_company_roles(self, company) -> list[CompanyRole]:
        """Récupère les rôles d'une entreprise donnée pour cet utilisateur"""
        qs1 = self.supervisor_roles.filter(company=company)
        qs2 = self.declarant_roles.filter(company=company)
        # L'union ne fonctionne pas car les objets ayant les même attributs,
        # Django applique un distinct() dessus, même si ces derniers ne sont pas du même type.
        return list(qs1) + list(qs2)

    def get_roles_mapped_to_companies(self) -> dict[int, list[CompanyRole]]:
        """Retourne les différents rôles d'un utilisateur pour chacune des entreprises à laquelle il est lié"""
        all_companies = self.declarable_companies.all().union(self.supervisable_companies.all())
        return {company: self.get_company_roles(company) for company in all_companies}

    def get_all_roles(self, company) -> list[BaseGlobalRole | CompanyRole]:
        """Récupère l'ensemble des rôles globaux et rôles liés à l'entreprise donnée pour cet utilisateur"""
        return self.get_global_roles() + self.get_company_roles(company)

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

    @property
    def name(self) -> str:
        """Syntaxic sugar"""
        return self.get_full_name()

    def __str__(self):
        return self.name
