import re
from django.core.exceptions import ValidationError


def validate_siret(value):
    """Validateur pour les numéros de SIRET"""
    if not value.isdigit() or len(value) != 14:
        raise ValidationError(
            "%(value)s n'est pas un SIRET valide. Il doit contenir 14 chiffres.",
            params={"value": value},
        )


def validate_vat(value):
    """Validateur pour les numéros de TVA intracommunautaires"""
    if not re.match(r"^[A-Z]{2}\d{2,12}$", value):
        raise ValidationError(
            "%(value)s n’est pas un numéro de TVA valide. Un numéro de TVA doit commencer par 2 lettres suivies de 2 à 12 chiffres.",
            params={"value": value},
        )
