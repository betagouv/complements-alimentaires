from datetime import timedelta as td
from urllib.parse import urlencode

from django.db import transaction
from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.manager import Manager

from data.behaviours import AutoValidable, TimeStampable, Expirable, ExpirableQuerySet
from ..mixins.unique_secret_key import UniqueSecretKeyMixin


class MagicLinkUsage(models.TextChoices):

    # First tuple item represents the front-end URI to be accessed
    VERIFY_EMAIL_ADDRESS = ("verification-email", "Verify email address")
    # ... add more usages here


class MagicLinkTokenQuerySet(ExpirableQuerySet):
    def for_email_verification(self):
        return self.filter(usage=MagicLinkUsage.VERIFY_EMAIL_ADDRESS)


class MagicLinkToken(UniqueSecretKeyMixin, TimeStampable, Expirable, AutoValidable, models.Model):
    """Token received by a user to identify an action (like verifying its email)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="magiclink_tokens")
    usage = models.CharField(max_length=1024, choices=MagicLinkUsage.choices)

    VALIDITY_TIME = td(weeks=1)

    objects = Manager.from_queryset(MagicLinkTokenQuerySet)()

    def as_url(self, **query_params) -> str:
        """Return the magink link url, as a suffix (to be joined to the base url)"""

        return f"{self.usage.value}/?{urlencode(query_params)}"

    @classmethod
    def run_email_verification(cls, input_key: str):
        """Given a key, try to find and consume an existing valid token.
        If challenge successful, mark the user confirmed and return it, None otherwise."""

        try:
            token = cls.objects.unexpired().for_email_verification().get(key=input_key)
        except cls.DoesNotExist:
            return None
        else:
            user = token.user
            with transaction.atomic():
                user.verify()
                token.delete()
            return user

    def __str__(self):
        return f"{self.user} 🔑 {self.key}"
