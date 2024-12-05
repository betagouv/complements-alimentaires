from enum import auto

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from data.behaviours import AutoValidable, Deactivable
from data.choices import CountryChoices
from data.fields import MultipleChoiceField
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


class CompanyContact(models.Model):
    class Meta:
        abstract = True

    phone_number = PhoneNumberField("numéro de téléphone de contact")
    email = models.EmailField("adresse e-mail de contact")
    website = models.CharField("site web de l'entreprise", blank=True)


class ActivityChoices(models.TextChoices):
    FABRICANT = auto()
    FAÇONNIER = auto()
    IMPORTATEUR = auto()
    INTRODUCTEUR = auto()
    CONSEIL = auto()
    DISTRIBUTEUR = auto()


class Company(AutoValidable, Address, CompanyContact, models.Model):
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
    activities = MultipleChoiceField(models.CharField(choices=ActivityChoices), verbose_name="activités", default=list)

    supervisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="SupervisorRole",
        blank=True,
        verbose_name="gestionnaires",
        related_name="supervisable_companies",
    )
    declarants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="DeclarantRole",
        blank=True,
        verbose_name="déclarants",
        related_name="declarable_companies",
    )
    mandated_companies = models.ManyToManyField(
        "self",
        blank=True,
        verbose_name="Autres entreprises pouvant déclarer pour cette entreprise",
        related_name="represented_companies",
        symmetrical=False,
    )

    def clean(self):
        # SIRET ou VAT ou les deux
        if not (self.siret or self.vat):
            raise ValidationError(
                "Une entreprise doit avoir un n° de SIRET ou un n°de TVA intracommunautaire (ou les deux)."
            )

        # Pas de duplication possible des activités
        if len(self.activities) != len(set(self.activities)):
            raise ValidationError("Une entreprise ne peut avoir plusieurs fois la même activité")

    @property
    def collaborators(self):
        """Retourne l'ensemble des objets `User` ayant au moins un rôle dans cette entreprise"""
        return self.supervisors.all().union(self.declarants.all())

    def __str__(self):
        return self.social_name


class CompanyRoleClassChoices(models.TextChoices):
    DeclarantRole = auto()
    SupervisorRole = auto()


class CompanyRole(Deactivable):
    """Réprésente un rôle d'utilisateur qui n'a de sens que pour une entreprise donnée"""

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.activity_icon} {self.user} ➔ {self.company}"


class SupervisorRole(CompanyRole, models.Model):
    class Meta:
        verbose_name = "rôle gestionnaire"
        verbose_name_plural = "rôles gestionnaire"
        unique_together = ("company", "user")

    company = models.ForeignKey(Company, related_name="supervisor_roles", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="supervisor_roles", on_delete=models.CASCADE)


class DeclarantRole(CompanyRole, models.Model):
    class Meta:
        verbose_name = "rôle déclarant"
        verbose_name_plural = "rôles déclarant"
        unique_together = ("company", "user")

    company = models.ForeignKey(Company, related_name="declarant_roles", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="declarant_roles", on_delete=models.CASCADE)
