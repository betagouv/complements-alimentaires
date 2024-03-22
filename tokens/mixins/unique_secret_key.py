import secrets

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UniqueSecretKeyMixin(models.Model):
    """Add fields and features related to a unique generated key."""

    class Meta:
        abstract = True

    key = models.CharField(primary_key=True, max_length=512, unique=True, editable=False)

    def _build_key(self) -> str:
        return secrets.token_urlsafe(32)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.key = self._build_key()
        super().save(*args, **kwargs)
