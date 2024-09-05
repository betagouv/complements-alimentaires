import json
import logging
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models import Case, Value, When
from django.db.models.functions import Coalesce
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from dateutil.relativedelta import relativedelta
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

logger = logging.getLogger(__name__)


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

    class Article(models.TextChoices):
        ARTICLE_15 = "ART_15", "Article 15"
        ARTICLE_15_WARNING = "ART_15_WARNING", "Article 15 Vigilance"
        ARTICLE_16 = "ART_16", "Article 16"
        ARTICLE_17 = "ART_17", "Article 17"

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
    other_galenic_formulation = models.TextField(blank=True, verbose_name="autre forme galénique non listée")

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
    other_conditions = models.TextField(
        blank=True, verbose_name="autres populations à risques ou facteurs de risques non listés"
    )

    effects = models.ManyToManyField(Effect, blank=True, verbose_name="objectifs ou effets")
    other_effects = models.TextField(blank=True, verbose_name="autres objectifs ou effets non listés")

    calculated_article = models.TextField("article calculé automatiquement", blank=True, choices=Article)
    overriden_article = models.TextField("article manuellement spécifié", blank=True, choices=Article)
    article = models.GeneratedField(
        expression=Coalesce(
            Case(When(overriden_article="", then=Value(None)), default="overriden_article"),
            Case(When(calculated_article="", then=Value(None)), default="calculated_article"),
            Value(None),
        ),
        output_field=models.TextField(verbose_name="article", null=True),
        db_persist=True,
    )

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

    @property
    def brevo_parameters(self):
        """
        Dictionnaire utilisé dans les différentes communications emails avec
        l'API Brevo
        """
        try:
            expiration_days = (
                self.snapshots.filter(
                    status__in=[
                        Declaration.DeclarationStatus.OBSERVATION,
                        Declaration.DeclarationStatus.OBJECTION,
                    ]
                )
                .latest("creation_date")
                .expiration_days
            )
        except Exception as _:
            expiration_days = ""
        return {
            "PRODUCT_NAME": self.name,
            "COMPANY_NAME": self.company.social_name if self.company else "",
            "DECLARATION_LINK": self.producer_url,
            "DECLARATION_ID": self.id,
            "EXPIRATION_DAYS": expiration_days,
        }

    @property
    def expiration_date(self):
        expirable_statuses = [
            Declaration.DeclarationStatus.OBJECTION,
            Declaration.DeclarationStatus.OBSERVATION,
            Declaration.DeclarationStatus.ABANDONED,
        ]
        if self.status not in expirable_statuses:
            return None
        try:
            latest_snapshot = self.snapshots.filter(
                status__in=[
                    Declaration.DeclarationStatus.OBJECTION,
                    Declaration.DeclarationStatus.OBSERVATION,
                ]
            ).latest("creation_date")
            expiration_date = latest_snapshot.creation_date + timedelta(days=latest_snapshot.expiration_days)
            return expiration_date
        except Exception as _:
            return None

    @property
    def response_limit_date(self):
        """
        La date limite d'instruction est fixée à deux mois à partir du dernier statut
        "en attente d'instruction"
        """
        concerned_statuses = [
            Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
            Declaration.DeclarationStatus.AWAITING_VISA,
            Declaration.DeclarationStatus.ONGOING_VISA,
        ]
        if self.status not in concerned_statuses:
            return None
        status = Declaration.DeclarationStatus.AWAITING_INSTRUCTION
        try:
            latest_snapshot = self.snapshots.filter(status=status).latest("creation_date")
            response_limit = latest_snapshot.creation_date + relativedelta(months=2)
            return response_limit
        except Exception as _:
            return None

    def __str__(self):
        return f"Déclaration « {self.name} »"

    def assign_article(self):
        """
        Cette fonction est appelée depuis les signals post_save et post_delete des objets calulated_<type>
        afin de mettre à jour l'article de la déclaration.
        Ces signals sont dans la fonction « update_article » de ce même fichier.
        """
        try:
            current_calculated_article = self.calculated_article
            new_calculated_article = current_calculated_article
            composition_items = (
                self.declared_plants,
                self.declared_microorganisms,
                self.declared_substances,
                self.declared_ingredients,
            )
            empty_composition = all(not x.exists() for x in composition_items)
            has_new_items = any(x.filter(new=True).exists() for x in composition_items if issubclass(x.model, Addable))
            surpasses_max_dose = any(
                x.quantity > x.substance.max_quantity
                for x in self.computed_substances.all()
                if x.substance.max_quantity and x.substance.unit == x.unit
                # TODO: vérifier si ce cas est possible, sinon enlever l'unit du ComputedSubstance
            )

            if empty_composition:
                new_calculated_article = ""
            elif surpasses_max_dose:
                new_calculated_article = Declaration.Article.ARTICLE_17
            elif has_new_items:
                new_calculated_article = Declaration.Article.ARTICLE_16
            else:
                new_calculated_article = Declaration.Article.ARTICLE_15

            if new_calculated_article != current_calculated_article:
                self.calculated_article = new_calculated_article
                self.save()
        except Exception as e:
            logger.error("Error calculating article")
            logger.exception(e)


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
    class Meta:
        verbose_name = "plante déclarée"
        verbose_name_plural = "plantes déclarées"

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

    def __str__(self):
        return f"{self.new_name or self.plant.name}"


class DeclaredMicroorganism(Historisable, Addable):
    class Meta:
        verbose_name = "microorganisme déclaré"
        verbose_name_plural = "microorganismes déclarés"

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

    def __str__(self):
        if self.new:
            return f"{self.new_species} {self.new_genre}"
        return f"{self.microorganism.species} {self.microorganism.genus}"


class DeclaredIngredient(Historisable, Addable):
    class Meta:
        verbose_name = "ingredient déclaré"
        verbose_name_plural = "ingredients déclarés"

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

    def __str__(self):
        return f"{self.new_name or self.ingredient.name}"


class DeclaredSubstance(Historisable):
    class Meta:
        verbose_name = "substance déclarée"
        verbose_name_plural = "substances déclarées"

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

    def __str__(self):
        return f"{self.substance.name}"


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


@receiver((post_save, post_delete), sender=DeclaredPlant)
@receiver((post_save, post_delete), sender=DeclaredMicroorganism)
@receiver((post_save, post_delete), sender=DeclaredSubstance)
@receiver((post_save, post_delete), sender=DeclaredIngredient)
@receiver((post_save, post_delete), sender=ComputedSubstance)
def update_article(sender, instance, *args, **kwargs):
    instance.declaration.assign_article()
