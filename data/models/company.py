from django.db import models
from django.core.exceptions import ValidationError
from data.behaviours import AutoValidable
from data.choices import CountryChoices
from data.validators import validate_siret, validate_vat


class Address(models.Model):
    # NOTE: à déplacer en dehors du modèle entreprise, si utilisable ailleurs
    class Meta:
        abstract = True

    address = models.CharField("adresse", help_text="numéro et voie")
    additional_details = models.CharField(
        "complément d’adresse",
        blank=True,
        null=False,
        help_text="bâtiment, immeuble, escalier et numéro d’appartement",
    )
    postal_code = models.CharField("code postal", max_length=10)
    city = models.CharField("ville ou commune")
    cedex = models.CharField("CEDEX", blank=True, null=False)
    country = models.CharField("pays", max_length=50, choices=CountryChoices, default=CountryChoices.FRANCE)

    @property
    def displayable_address(self):
        lines = [
            self.address,
            self.additional_details,
            f"{self.postal_code} {self.city}",
            self.cedex,
            self.get_country_display().upper(),
        ]
        return "\n".join(filter(None, lines))


class Company(AutoValidable, Address, models.Model):
    class Meta:
        verbose_name = "entreprise"

    social_name = models.CharField("dénomination sociale")
    commercial_name = models.CharField("enseigne", help_text="nom commercial")
    # null=True permet de gérer en parralèle le unique=True
    siret = models.CharField(
        "n° SIRET",
        help_text="14 chiffres",
        unique=True,
        blank=True,
        null=True,
        validators=[validate_siret],
    )
    vat = models.CharField("n° TVA intracommunautaire", unique=True, blank=True, null=True, validators=[validate_vat])

    def clean(self):
        if not (self.siret or self.vat):
            raise ValidationError(
                "Une entreprise doit avoir un n° de SIRET ou un n°de TVA intracommunautaire (ou les deux)."
            )

    def __str__(self):
        return self.social_name
