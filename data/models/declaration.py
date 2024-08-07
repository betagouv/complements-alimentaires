import json

from django.conf import settings
from django.db import models

from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from data.behaviours import Historisable, TimeStampable
from data.choices import AuthorizationModes, CountryChoices, FrAuthorizationReasons
from data.models import (
    Company,
    Condition,
    Effect,
    GalenicFormulation,
    Ingredient,
    InstructionRole,
    Microorganism,
    Plant,
    PlantPart,
    Population,
    Substance,
    SubstanceUnit,
    VisaRole,
)


class Declaration(Historisable, TimeStampable):
    class Meta:
        verbose_name = "déclaration"

    class DeclarationStatus(models.TextChoices):
        DRAFT = "DRAFT", "Brouillon"
        AWAITING_INSTRUCTION = "AWAITING_INSTRUCTION", "En attente d'instruction"
        ONGOING_INSTRUCTION = "ONGOING_INSTRUCTION", "Instruction en cours"
        AWAITING_VISA = "AWAITING_VISA", "En attente de visa"
        ONGOING_VISA = "ONGOING_VISA", "Visa en cours"
        OBJECTION = "OBJECTION", "En objection"
        OBSERVATION = "OBSERVATION", "En observation"
        ABANDONED = "ABANDONED", "Abandonnée"
        AUTHORIZED = "AUTHORIZED", "Autorisée"
        REJECTED = "REJECTED", "Refusée"
        WITHDRAWN = "WITHDRAWN", "Retiré du marché"

    class RejectionReason(models.TextChoices):
        MISSING_DATA = "MISSING_DATA", "Le dossier manque des données nécessaires"
        MEDICINE = "MEDICINE", "Le complément répond à la définition du médicament"
        INCOMPATIBLE_RECOMMENDATIONS = "INCOMPATIBLE_RECOMMENDATIONS", "Recommandations d'emploi incompatibles"

    status = models.CharField(
        max_length=50,
        choices=DeclarationStatus.choices,
        default=DeclarationStatus.DRAFT,
        verbose_name="status",
    )
    post_validation_status = models.CharField(
        max_length=50,
        blank=True,
        choices=DeclarationStatus.choices,
        default=DeclarationStatus.DRAFT,
        verbose_name="status à assigner après la validation",
    )
    post_validation_producer_message = models.TextField(
        blank=True,
        verbose_name="message à envoyer au producteur après la validation",
    )
    post_validation_expiration_days = models.IntegerField(
        null=True, blank=True, verbose_name="délai de réponse à assigner après la validation"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="auteur",
        related_name="declarations",
    )
    instructor = models.ForeignKey(
        InstructionRole,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="instructeur",
        related_name="declarations",
    )
    visor = models.ForeignKey(
        VisaRole,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="visor",
        related_name="declarations",
    )

    private_notes = models.TextField("notes à destination de l'administration", blank=True, default="")
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
    postal_code = models.CharField("code postal", blank=True, max_length=10)
    city = models.TextField("ville ou commune", blank=True)
    cedex = models.TextField("CEDEX", blank=True)
    country = models.TextField("pays", blank=True, choices=CountryChoices)

    name = models.TextField(blank=True, verbose_name="nom du produit")
    brand = models.TextField(blank=True, verbose_name="marque")
    gamme = models.TextField(blank=True, verbose_name="gamme")
    flavor = models.TextField(blank=True, verbose_name="arôme")
    description = models.TextField(blank=True, verbose_name="description")

    galenic_formulation = models.ForeignKey(
        GalenicFormulation, verbose_name="forme galénique", null=True, blank=True, on_delete=models.RESTRICT
    )

    unit_quantity = models.FloatField(
        null=True, blank=True, verbose_name="poids ou volume d'une unité de consommation"
    )
    unit_measurement = models.ForeignKey(
        SubstanceUnit,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        verbose_name="unité de mesure pour une unité de consommation",
    )

    conditioning = models.TextField(blank=True, verbose_name="conditionnement")
    daily_recommended_dose = models.TextField(blank=True, verbose_name="dose journalière recommandée")
    minimum_duration = models.TextField(blank=True, verbose_name="durabilité minimale / DLUO (en mois)")

    instructions = models.TextField(blank=True, verbose_name="mode d'emploi")
    warning = models.TextField(blank=True, verbose_name="mise en garde et avertissement")

    populations = models.ManyToManyField(Population, blank=True, verbose_name="populations cibles")
    conditions_not_recommended = models.ManyToManyField(
        Condition, blank=True, verbose_name="consommation déconseillée"
    )

    effects = models.ManyToManyField(Effect, blank=True, verbose_name="objectifs ou effets")
    other_effects = models.TextField(blank=True, verbose_name="autres objectifs ou effets non-listés")

    def create_snapshot(
        self,
        user=None,
        comment="",
        action=None,
        post_validation_status="",
        expiration_days=None,
        blocking_reasons=None,
    ):
        # Sinon on a des imports circulaires
        from data.factories import SnapshotFactory
        from data.models import Snapshot

        SnapshotFactory.create(
            declaration=self,
            user=user,
            status=self.status,
            json_declaration=self.json_representation,
            expiration_days=expiration_days,
            comment=comment,
            action=action or Snapshot.SnapshotActions.OTHER,
            post_validation_status=post_validation_status,
            blocking_reasons=blocking_reasons,
        )

    @property
    def json_representation(self):
        from api.serializers import DeclarationSerializer

        serialized_data = DeclarationSerializer(self).data
        camelized_bytes = CamelCaseJSONRenderer().render(serialized_data)
        return json.loads(camelized_bytes.decode("utf-8"))

    @property
    def producer_url(self):
        return f"{'https' if settings.SECURE else 'http'}://{settings.HOSTNAME}/mes-declarations/{self.id}"

    def __str__(self):
        return f"Déclaration « {self.name} »"


# Les modèles commençant par `Declared` représentent des éléments ajoutés par l'utilisateur.ice dans sa
# déclaration. Ces éléments peuvent être choisis dans la base de données ou rajoutés manuellement.
# Un élément ajouté manuellement peut être identifié comme étant déjà en base, dans ce cas la ForeignKey
# et les champs de l'utilisateur.ice seront présents.


class Addable(models.Model):
    class Meta:
        abstract = True

    new = models.BooleanField(default=False)
    new_description = models.TextField(blank=True, verbose_name="description")

    authorization_mode = models.CharField(
        choices=AuthorizationModes.choices,
        blank=True,
        verbose_name="modalité d'autorisation pour un élément ajouté manuellement",
    )
    fr_reason = models.CharField(
        choices=FrAuthorizationReasons.choices,
        blank=True,
        verbose_name="raison de l'ajout manuel",
    )
    fr_details = models.CharField("information additionnelle sur l'autorisation en France", blank=True)
    eu_reference_country = models.CharField(
        "pays de source réglementaire", blank=True, choices=CountryChoices, default=CountryChoices.FRANCE
    )
    eu_legal_source = models.TextField("référence du texte réglementaire d'un autre pays européen", blank=True)
    eu_details = models.TextField(
        "information additionnelle sur l'autorisation dans un autre pays européen", blank=True
    )


class DeclaredPlant(Historisable, Addable):
    declaration = models.ForeignKey(
        Declaration,
        related_name="declared_plants",
        verbose_name=Declaration._meta.verbose_name,
        on_delete=models.CASCADE,
    )
    plant = models.ForeignKey(
        Plant, null=True, blank=True, verbose_name="plante ajoutée par l'utilisateur", on_delete=models.RESTRICT
    )
    active = models.BooleanField("ayant une activité physiologique ou nutritionnelle", default=True)
    new_name = models.TextField(blank=True, verbose_name="nom de la plante ajoutée manuellement")

    used_part = models.ForeignKey(
        PlantPart, null=True, blank=True, verbose_name="partie utilisée", on_delete=models.RESTRICT
    )
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR")
    unit = models.ForeignKey(SubstanceUnit, null=True, blank=True, verbose_name="unité", on_delete=models.RESTRICT)
    preparation = models.TextField(blank=True, verbose_name="préparation")


class DeclaredMicroorganism(Historisable, Addable):
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
    active = models.BooleanField("ayant une activité physiologique ou nutritionnelle", default=True)
    activated = models.BooleanField("n'ayant pas été inactivé (rendu incapable de réplication)", default=True)
    new_species = models.TextField(blank=True, verbose_name="espèce du micro-organisme ajouté manuellement")
    new_genre = models.TextField(blank=True, verbose_name="genre du micro-organisme ajoutée manuellement")

    strain = models.TextField(blank=True, verbose_name="souche")
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR (en UFC)")


class DeclaredIngredient(Historisable, Addable):
    declaration = models.ForeignKey(
        Declaration,
        related_name="declared_ingredients",
        verbose_name=Declaration._meta.verbose_name,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient, null=True, blank=True, verbose_name="ingrédient ajouté par l'user", on_delete=models.RESTRICT
    )
    active = models.BooleanField("ayant une activité physiologique ou nutritionnelle", default=True)
    new_name = models.TextField(blank=True, verbose_name="libellé")
    new_type = models.TextField(blank=True, verbose_name="type de l'ingrédient")
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR")
    unit = models.ForeignKey(SubstanceUnit, null=True, blank=True, verbose_name="unité", on_delete=models.RESTRICT)


class DeclaredSubstance(Historisable):
    declaration = models.ForeignKey(
        Declaration,
        related_name="declared_substances",
        verbose_name=Declaration._meta.verbose_name,
        on_delete=models.CASCADE,
    )
    active = models.BooleanField("ayant une activité physiologique ou nutritionnelle", default=True)
    substance = models.ForeignKey(
        Substance, null=True, blank=True, verbose_name="substance ajoutée par l'user", on_delete=models.RESTRICT
    )


# Les substances détectées au moment de faire la déclaration seront ici, avec la valeur de la quantité
# mise par l'utilisateur.ice comprenant la totalité du complément (çad en incluant tous les éléments qui
# la contiennent


class ComputedSubstance(Historisable):
    declaration = models.ForeignKey(
        Declaration,
        related_name="computed_substances",
        verbose_name=Declaration._meta.verbose_name,
        on_delete=models.CASCADE,
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
        Declaration, related_name="attachments", verbose_name=Declaration._meta.verbose_name, on_delete=models.CASCADE
    )
    file = models.FileField(
        null=True, blank=True, upload_to="declaration-attachments/%Y/%m/%d/", verbose_name="pièce jointe"
    )
    name = models.TextField("nom du fichier", blank=True)
