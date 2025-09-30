from django.conf import settings
from django.db import models

from data.behaviours import Deactivable, DeactivableQuerySet


class GlobalRoleManager(models.Manager):
    pass


class BaseGlobalRoleQuerySet(DeactivableQuerySet):
    pass


class BaseGlobalRole(Deactivable, models.Model):
    """Un rôle global est un rôle uniquement lié à l'utilisateur."""

    class Meta:
        abstract = True

    objects = GlobalRoleManager().from_queryset(BaseGlobalRoleQuerySet)()

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="utilisateur",
        on_delete=models.CASCADE,
    )

    @property
    def name(self) -> str:
        return self.user.name

    def __str__(self):
        return self.name


class InstructionRole(BaseGlobalRole):
    class Meta:
        verbose_name = "rôle instruction"
        verbose_name_plural = "rôles instruction"


class VisaRole(BaseGlobalRole):
    class Meta:
        verbose_name = "rôle de visa"
        verbose_name_plural = "rôles de visa"


class ControlRole(BaseGlobalRole):
    always_persist = models.BooleanField(
        default=False,
        verbose_name="toujours maintenir le rôle",
        help_text="Ce rôle ne sera pas retiré lors des synchronisations automatiques",
    )

    class Meta:
        verbose_name = "rôle de contrôle"
        verbose_name_plural = "rôles de contrôle"


class ControlRoleEmail(models.Model):
    """
    Cette liste contient les emails des personnes qui doivent avoir le rôle ControlRole.
    """

    email = models.EmailField(unique=True, verbose_name="email autorisé")
    created_at = models.DateTimeField(auto_now_add=True)
