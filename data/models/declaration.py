from django.db import models
from django.conf import settings
from data.behaviours import Historisable, TimeStampable
from data.choices import CountryChoices
from data.models import (
    SubstanceUnit,
    Population,
    Condition,
    Plant,
    Microorganism,
    Ingredient,
    Substance,
    PlantPart,
    Company,
)
from django.contrib.postgres.fields import ArrayField


class Declaration(Historisable, TimeStampable):

    class Meta:
        verbose_name = "déclaration"

    class DiagnosticStatus(models.TextChoices):
        DRAFT = "DRAFT", "Déclaration"
        AWAITING_INSTRUCTION = "AWAITING_INSTRUCTION", "En attente de retour instruction"
        AWAITING_PRODUCER = "AWAITING_PRODUCER", "En attente de retour du déclarant"
        REJECTED = "REJECTED", "Rejeté"
        APPROVED = "APPROVED", "Validé"

    class RejectionReason(models.TextChoices):
        MISSING_DATA = "MISSING_DATA", "Le dossier manque des données nécessaires"
        MEDICINE = "MEDICINE", "Le complément répond à la définition du médicament"
        INCOMPATIBLE_RECOMMENDATIONS = "INCOMPATIBLE_RECOMMENDATIONS", "Recommandations d'emploi incompatibles"

    status = models.CharField(
        max_length=50,
        choices=DiagnosticStatus.choices,
        default=DiagnosticStatus.DRAFT,
        verbose_name="Status",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="auteur",
        related_name="declarations",
    )
    company = models.ForeignKey(
        Company, null=True, on_delete=models.SET_NULL, verbose_name="entreprise", related_name="declarations"
    )

    # Champs adresse :
    # On ne prend pas la même classe que l'adresse de la compagnie car on a besoin
    # d'avoir ces champs facultatifs
    address = models.TextField("adresse", blank=True, help_text="numéro et voie")
    additional_details = models.TextField(
        "complément d’adresse",
        blank=True,
        help_text="bâtiment, immeuble, escalier et numéro d’appartement",
    )
    postal_code = models.TextField("code postal", blank=True, max_length=10)
    city = models.TextField("ville ou commune", blank=True)
    cedex = models.TextField("CEDEX", blank=True)
    country = models.TextField("pays", blank=True, choices=CountryChoices)

    name = models.TextField(blank=True, verbose_name="nom du produit")
    brand = models.TextField(blank=True, verbose_name="marque")
    gamme = models.TextField(blank=True, verbose_name="gamme")
    flavor = models.TextField(blank=True, verbose_name="arôme")
    description = models.TextField(blank=True, verbose_name="description")
    #########

    galenic_formulation = models.TextField(
        blank=True, verbose_name="forme galénique"
    )  # TODO : à terme mettre des valeurs de la DB
    unit_quantity = models.FloatField(null=True, verbose_name="poids ou volume d'une unité de consommation")
    unit_measurement = models.ForeignKey(
        SubstanceUnit,
        null=True,
        on_delete=models.RESTRICT,
        verbose_name="unité de mesure pour une unité de consommation",
    )

    conditioning = models.TextField(blank=True, verbose_name="conditionnements")
    daily_recommended_dose = models.TextField(blank=True, verbose_name="dose journalière recommandée")
    minimum_duration = models.TextField(blank=True, verbose_name="durabilité minimale / DLUO (en mois)")

    instructions = models.TextField(blank=True, verbose_name="mode d'emploi")
    warning = models.TextField(blank=True, verbose_name="mise en garde et avertissement")

    populations = models.ManyToManyField(Population, blank=True, verbose_name="populations cible")
    conditions_not_recommended = models.ManyToManyField(Condition, verbose_name="consommation déconseillée")

    # TODO : à transformer dans un champ avec ForeignKey une fois qu'on aura les effets dans notre DB
    effects = ArrayField(
        base_field=models.TextField(), blank=True, null=True, size=None, verbose_name="objectifs ou effets"
    )
    other_effects = models.TextField(blank=True, verbose_name="autres objectifs ou effets non-listés")


# Les modèles commençant par `Declared` représentent des éléments ajoutés par l'utilisateur.ice dans sa
# déclaration. Ces éléments peuvent être choisis dans la base de données ou rajoutés manuellement.
# Un élément ajouté manuellement peut être identifié comme étant déjà en base, dans ce cas la ForeignKey
# et les champs de l'utilisateur.ice seront présents.


class DeclaredPlant(Historisable):
    declaration = models.ForeignKey(
        Declaration, related_name="declared_plants", verbose_name="déclaration", on_delete=models.CASCADE
    )
    plant = models.ForeignKey(
        Plant, null=True, blank=True, verbose_name="plante ajoutée par l'user", on_delete=models.RESTRICT
    )

    new = models.BooleanField(default=False)
    new_name = models.TextField(blank=True, verbose_name="nom de la plante ajoutée manuellement")
    new_description = models.TextField(blank=True, verbose_name="description de la plante ajoutée manuellement")

    active = models.BooleanField(default=True)
    used_part = models.ForeignKey(
        PlantPart, null=True, blank=True, verbose_name="partie utilisée", on_delete=models.RESTRICT
    )
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR")
    unit = models.ForeignKey(SubstanceUnit, null=True, blank=True, verbose_name="unité", on_delete=models.RESTRICT)
    preparation = models.TextField(blank=True, verbose_name="préparation")


class DeclaredMicroorganism(Historisable):
    declaration = models.ForeignKey(
        Declaration, related_name="declared_microorganisms", verbose_name="déclaration", on_delete=models.CASCADE
    )
    microorganism = models.ForeignKey(
        Microorganism,
        null=True,
        blank=True,
        verbose_name="microorganisme ajouté par l'user",
        on_delete=models.RESTRICT,
    )

    new = models.BooleanField(default=False)

    # TODO : Update fields after merging of #339
    new_name = models.TextField(blank=True, verbose_name="nom du micro-organisme ajoutée manuellement")
    new_genre = models.TextField(blank=True, verbose_name="genre du micro-organisme ajoutée manuellement")
    new_description = models.TextField(blank=True, verbose_name="description du micro-organisme ajoutée manuellement")

    active = models.BooleanField(default=True)
    souche = models.TextField(blank=True, verbose_name="souche")
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR (en CFU)")


class DeclaredIngredient(Historisable):
    declaration = models.ForeignKey(
        Declaration, related_name="declared_ingredients", verbose_name="déclaration", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, null=True, blank=True, verbose_name="ingrédient ajouté par l'user", on_delete=models.RESTRICT
    )

    new = models.BooleanField(default=False)
    new_name = models.TextField(blank=True, verbose_name="libellé")
    new_description = models.TextField(blank=True, verbose_name="description")

    active = models.BooleanField(default=True)


class DeclaredSubstance(Historisable):
    declaration = models.ForeignKey(
        Declaration, related_name="declared_substances", verbose_name="déclaration", on_delete=models.CASCADE
    )
    substance = models.ForeignKey(
        Substance, null=True, blank=True, verbose_name="substance ajoutée par l'user", on_delete=models.RESTRICT
    )
    active = models.BooleanField(default=True)


# Les substances détectées au moment de faire la déclaration seront ici, avec la valeur de la quantité
# mise par l'utilisateur.ice comprenant la totalité du complément (çad en incluant tous les éléments qui
# la contiennent


class ComputedSubstance(Historisable):
    declaration = models.ForeignKey(
        Declaration, related_name="computed_substances", verbose_name="déclaration", on_delete=models.CASCADE
    )
    substance = models.ForeignKey(
        Substance, null=True, blank=True, verbose_name="substance ajoutée par l'user", on_delete=models.RESTRICT
    )
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR")
    unit = models.ForeignKey(SubstanceUnit, null=True, blank=True, verbose_name="unité", on_delete=models.RESTRICT)


# Les pièces jointes peuvent avoir plusieurs types et formats.


class Attachment(Historisable):
    class AttachmentType(models.TextChoices):
        LABEL = "LABEL", "Étiquetage"
        REGULATORY_PROOF = "REGULATORY_PROOF", "Preuve règlementaire"
        CERTIFICATE_AUTHORITY = "CERTIFICATE_AUTHORITY", "Attestation d'une autorité compétente"
        ADDITIONAL_INFO = (
            "ADDITIONAL_INFO",
            "Compléments info professionnel",
        )
        OBSERVATIONS = (
            "OBSERVATIONS",
            "Observations professionnel",
        )
        PROFESSIONAL_MAIL = (
            "PROFESSIONAL_MAIL",
            "Autre courrier du professionnel",
        )
        DRAFT = (
            "DRAFT",
            "Brouillon",
        )
        OTHER = (
            "OTHER",
            "Autre professionnel",
        )
        ANALYSIS_REPORT = (
            "ANALYSIS_REPORT",
            "Bulletin d'analyse",
        )

    type = models.CharField(
        max_length=50,
        choices=AttachmentType.choices,
        null=True,
        blank=True,
        verbose_name="type",
    )
    declaration = models.ForeignKey(
        Declaration, related_name="attachments", verbose_name="déclaration", on_delete=models.CASCADE
    )
    file = models.FileField(
        null=True, blank=True, upload_to="declaration-attachments/%Y/%m/%d/", verbose_name="pièce jointe"
    )
