from enum import auto

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from data.behaviours import AutoValidable, Deactivable, TimeStampable
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

    @property
    def department(self):
        if self.country != CountryChoices.FRANCE:
            return None

        if self.postal_code[:2] == "97" or self.postal_code[:2] == "98":
            return self.postal_code[:3]

        # Cas pour la corse : Corse du Sud : 2A, Corse du Nord : 2B
        if self.postal_code[:2] == "20":
            corsica_identifier = self.postal_code[2:3]
            return "2A" if corsica_identifier == "0" or corsica_identifier == "1" else "2B"

        return self.postal_code[:2]


class CompanyContact(models.Model):
    class Meta:
        abstract = True

    phone_number = PhoneNumberField("numéro de téléphone de contact", blank=True)
    email = models.EmailField("adresse e-mail de contact", blank=True)
    website = models.CharField("site web de l'entreprise", blank=True)


class ActivityChoices(models.TextChoices):
    FABRICANT = auto()
    FAÇONNIER = auto()
    IMPORTATEUR = auto()
    INTRODUCTEUR = auto()
    CONSEIL = auto()
    DISTRIBUTEUR = auto()


class Company(AutoValidable, Address, CompanyContact, TimeStampable, models.Model):
    class Meta:
        verbose_name = "entreprise"

    social_name = models.CharField("dénomination sociale")
    commercial_name = models.CharField("enseigne", blank=True, help_text="nom commercial")
    # null=True permet de gérer en parralèle le unique=True
    siret = models.CharField(
        "n° SIRET",
        help_text="14 chiffres",
        unique=True,
        null=True,
        blank=True,  # nécessaire pour valider les données issues de l'admin form, avec la méthode custom save()
        validators=[validate_siret],
    )
    vat = models.CharField(
        "n° TVA intracommunautaire",
        unique=True,
        null=True,
        blank=True,  # nécessaire pour valider les données issues de l'admin form, avec la méthode custom save()
        validators=[validate_vat],
    )
    activities = MultipleChoiceField(
        models.CharField(choices=ActivityChoices), verbose_name="activités", default=list, blank=True
    )

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
        # Au minimum un point de contact nécessaire (hors None ou "")
        if not ((self.phone_number and self.phone_number.is_valid()) or self.email):
            raise ValidationError("Une entreprise doit avoir un n° de téléphone ou un e-mail (ou les deux).")
        # Pas de duplication possible des activités
        if len(self.activities) != len(set(self.activities)):
            raise ValidationError("Une entreprise ne peut avoir plusieurs fois la même activité")

    @property
    def registration_date(self):
        """Retourne la plus ancienne date d'adhésion à la déclaration en ligne
        * soit date de première adhésion à TeleIcare,
        soit date d'adhésion à Compl'Alim"""
        return self.etablissementtocompanyrelation_set.earliest("siccrf_registration_date") or self.creation_date

    @property
    def collaborators(self):
        """Retourne l'ensemble des objets `User` ayant au moins un rôle dans cette entreprise"""
        return self.supervisors.all().union(self.declarants.all())

    def __str__(self):
        return self.social_name

    def save(self, *args, **kwargs):
        # Les valeurs "" ne sont pas unique, mais None oui
        if not self.vat:
            self.vat = None
        if not self.siret:
            self.siret = None
        super().save(*args, **kwargs)


class CompanyRoleClassChoices(models.TextChoices):
    DeclarantRole = auto()
    SupervisorRole = auto()


class CompanyRole(Deactivable):
    """Représente un rôle d'utilisateur qui n'a de sens que pour une entreprise donnée"""

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


class EtablissementToCompanyRelation(models.Model):
    class Meta:
        verbose_name = "Anciens n° SIRET et n° TVA intracommunautaire, relation avec table d'entreprises TeleIcare et les entreprises Compl'Alim"

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # ce champ devrait être une ForeignKey vers la table unmanaged IcaEtablissement
    # mais une ForeignKey vers une table unmanaged implique de cla complexité au niveau du code :
    # création des tables au setup des tests notamment
    # https://docs.djangoproject.com/fr/5.1/ref/models/options/#managed

    siccrf_id = models.IntegerField(
        verbose_name="etab_ident dans le modèle IcaEtablissement SICCRF",
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        default=None,
    )
    old_siret = models.CharField(
        verbose_name="n° SIRET dans TeleIcare, si différent",
        unique=True,
        null=True,
        blank=True,  # nécessaire pour valider les données issues de l'admin form, avec la méthode custom save()
        validators=[validate_siret],
        help_text="14 chiffres",
    )
    old_vat = models.CharField(
        verbose_name="n° TVA intracommunautaire dans TeleIcare, si différent",
        unique=True,
        null=True,
        blank=True,  # nécessaire pour valider les données issues de l'admin form, avec la méthode custom save()
        validators=[validate_vat],
    )
    siccrf_registration_date = models.DateField(
        verbose_name="date d'adhésion à la plateforme TeleIcare", editable=False, null=True
    )

    def save(self, *args, **kwargs):
        # Les valeurs "" ne sont pas unique, mais None oui
        if not self.old_vat:
            self.old_vat = None
        if not self.old_siret:
            self.old_siret = None
        super().save(*args, **kwargs)
