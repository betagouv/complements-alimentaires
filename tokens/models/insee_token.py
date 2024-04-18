from __future__ import annotations
import logging
import requests
from base64 import b64encode
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class InseeToken(models.Model):
    """
    Token (objet unique) permettant les requêtes aux APIs INSEE.
    Il est automatiquement mis à jour en cas d'invalidité.
    L'objet retourné peut ne pas être utilisable en cas d'échec du call API.
    Utilisation : `InseeToken.load()`
    """

    class Meta:
        verbose_name = "Token Insee"
        verbose_name_plural = "Token Insee"  # il ne peut pas y en avoir plusieurs

    key = models.CharField("clé", blank=True, null=True)  # si null, signifie que la clé n'a pas pu être récupérée
    expiration = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Pattern singleton : une seule instance de la classe peut exister"""
        self.pk = 1
        super().save(*args, **kwargs)

    @property
    def usable(self) -> bool:
        """Retourne True si le token peut être utilisé tel quel"""
        return self.key and self.expiration > timezone.now()

    @classmethod
    def load(cls) -> InseeToken:
        """Équivalent de get_or_create dans l'esprit, mais en appelant une logique de refetch du token en cas d'invalidité."""

        def _kwargs():
            # Durée de validité : 7 jours (moins 1h de délai par marge de sécurité)
            return dict(key=cls.try_fetch_insee_token(), expiration=timezone.now() + timedelta(seconds=604800 - 3600))

        try:
            obj = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            logger.info("no INSEE token found, a new (and unique) one will be created")
            obj = cls.objects.create(**_kwargs())
        else:
            logger.info("existing INSEE token has been found")
            if not obj.usable:
                logger.info("existing INSEE token is not usable, a new one will try to be fetched")
                obj = cls(**_kwargs())
                obj.save()

        return obj

    @staticmethod
    def try_fetch_insee_token() -> str | None:
        """Essaie de récupérer un token INSEE d'une durée de validation de 7 jours, et le renvoie si l'opération a réussi."""

        if not settings.INSEE_API_KEY or not settings.INSEE_API_SECRET:
            logger.info("skipping INSEE token fetching because key and secret env vars aren't both set")
            return None

        base64_credentials = b64encode(f"{settings.INSEE_API_KEY}:{settings.INSEE_API_SECRET}".encode()).decode()
        response = requests.post(
            settings.INSEE_TOKEN_API_URL,
            data={"grant_type": "client_credentials", "validity_period": 604800},  # 7 jours
            headers={"Authorization": f"Basic {base64_credentials}"},
        )

        if response.ok:
            return response.json()["access_token"]
        else:
            logger.warning(f"INSEE token fetching failed, code {response.status_code} : {response}")
            return None
