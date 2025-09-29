import re

from django.core.exceptions import ValidationError


def validate_siret(value):
    """
    Validateur pour les numéros de SIRET
    (https://portal.hardis-group.com/pages/viewpage.action?pageId=120357227)
    """
    if not value.isdigit() or len(value) != 14:
        raise ValidationError("Un numéro de SIRET valide doit contenir 14 chiffres.")
    odd_digits = [int(n) for n in value[-1::-2]]
    even_digits = [int(n) for n in value[-2::-2]]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(int(n) for n in str(digit * 2))
    luhn_checksum_valid = checksum % 10 == 0

    if not luhn_checksum_valid:
        raise ValidationError("Le numéro de SIRET n'est pas valide.")


def validate_vat(value):
    """Validateur pour les numéros de TVA intracommunautaires"""
    if not re.match(r"^[A-Z]{2,}\w{2,12}$", value):
        raise ValidationError(
            "Un numéro de TVA valide doit commencer par minimum 2 lettres suivies de 2 à 12 chiffres."
        )


def validate_cas(value):
    """Validateur pour les numéros CAS de substance"""
    if not re.match(r"^[0-9]{2,7}-[0-9]{2}-[0-9]{1}$", value):
        raise ValidationError(
            "Un numéro CAS valide doit se conformer au modèle XXXXXXX-YY-Z, chaque lettre représentant un chiffre. La première partie contient minimum 2 chiffres et maximum 7."
        )
