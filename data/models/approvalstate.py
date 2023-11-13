from django.db import models


class LegacyApprovalState(models.TextChoices):
    TO_REGISTER = "to_register", "À inscrire"
    AUTHORIZED = "authorized", "Autorisé"
    REJECTED = "rejected", "Non autorisé"
    UNKNOWN = "unknown", "Sans objet"
