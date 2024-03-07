from django.db import models, transaction

from django.conf import settings
from django.contrib.auth import get_user_model
from data.mixins import Deactivable


class RoleManager(models.Manager):
    @transaction.atomic
    def create_role(self, user_dict_kwargs=None, role_dict_kwargs=None):
        """
        Helper to create both role and user objects in one shot
        Note that this logic could live in a custom manager too.
        """
        User = get_user_model()
        new_user = User.objects.create_user(**user_dict_kwargs)
        return self.create(user=new_user, **role_dict_kwargs)


class BaseRole(Deactivable, models.Model):
    class Meta:
        abstract = True

    objects = RoleManager()

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


# class Declarant(BaseRole):
#     class Meta:
#         verbose_name = "déclarant"

#     some_field_dec = models.CharField("some field only related to declarant", blank=True)

#     def some_method_dec(self):
#         print("Je suis un déclarant !")


# class Gestionnaire(BaseRole):
#     class Meta:
#         verbose_name = "gestionnaire"

#     some_field_ges = models.CharField("some field only related to gestionnaire", blank=True)

#     def some_method_ges(self):
#         print("Je suis un gestionnaire !")
