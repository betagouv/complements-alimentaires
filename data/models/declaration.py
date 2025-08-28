import json
import logging
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Case, Min, Q, Value, When
from django.db.models.functions import Coalesce
from django.template.defaultfilters import filesizeformat
from django.utils.formats import date_format

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
    Preparation,
    Substance,
    SubstanceType,
    SubstanceUnit,
    VisaRole,
)
from data.models.ingredient_status import IngredientStatus
from data.models.substance import MaxQuantityPerPopulationRelation

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
        ARTICLE_15_HIGH_RISK_POPULATION = "ART_15_HIGH_RISK_POPULATION", "Article 15 Population à risque"
        ARTICLE_16 = "ART_16", "Article 16"
        # ARTICLE_17 = "ART_17", "Article 17"
        ARTICLE_18 = "ART_18", "Article 18"
        ANSES_REFERAL = "ANSES_REFERAL", "nécessite saisine ANSES"

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

    private_notes_instruction = models.TextField(
        "notes de l'instruction à destination de l'administration", blank=True, default=""
    )
    private_notes_visa = models.TextField("notes du visa à destination de l'administration", blank=True, default="")
    company = models.ForeignKey(
        Company, null=True, on_delete=models.SET_NULL, verbose_name="entreprise", related_name="declarations"
    )
    mandated_company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="entreprise mandataire",
        related_name="mandated_declarations",
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
    # TODO: les Article.choice pour overridden_article ne devraient pas inclure les choices calculés automatiquement
    overridden_article = models.TextField("article manuellement spécifié", blank=True, choices=Article)
    article = models.GeneratedField(
        expression=Coalesce(
            Case(When(overridden_article="", then=Value(None)), default="overridden_article"),
            Case(When(calculated_article="", then=Value(None)), default="calculated_article"),
            Value(None),
        ),
        output_field=models.TextField(verbose_name="article", null=True),
        db_persist=True,
    )
    siccrf_id = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        unique=True,
        verbose_name="identifiant Teleicare si la déclaration provient de Teleicare, IcaComplementAlimentaire.cplalim_ident",
    )
    teleicare_declaration_number = models.TextField(
        blank=True,
        null=True,
        editable=False,
        verbose_name="numéro de déclaration Teleicare connu par les déclarants et indiqué dans les attestations",
    )  # pas de contrainte d'unicité car dans 124 cas le teleicare_declaration_number est dupliqué

    def create_snapshot(
        self,
        user=None,
        comment="",
        action=None,
        post_validation_status="",
        expiration_days=None,
        blocking_reasons=None,
        effective_withdrawal_date=None,
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
            effective_withdrawal_date=effective_withdrawal_date,
        )

    @property
    def blocking_reasons(self):
        from data.models import Snapshot

        try:
            latest_snapshot = self.snapshots.filter(blocking_reasons__isnull=False).latest("creation_date")
            return latest_snapshot.blocking_reasons
        except Snapshot.DoesNotExist:
            return None

    @property
    def last_administration_comment(self):
        from data.models import Snapshot

        admin_actions = [
            Snapshot.SnapshotActions.OBSERVE_NO_VISA,
            Snapshot.SnapshotActions.AUTHORIZE_NO_VISA,
            Snapshot.SnapshotActions.REQUEST_VISA,
            Snapshot.SnapshotActions.ACCEPT_VISA,
            Snapshot.SnapshotActions.REFUSE_VISA,
        ]

        try:
            latest_snapshot = self.snapshots.filter(comment__isnull=False, action__in=admin_actions).latest(
                "creation_date"
            )
            return latest_snapshot.comment
        except Snapshot.DoesNotExist:
            return None

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
        status = Declaration.DeclarationStatus
        try:
            expiration_days = (
                self.snapshots.filter(status__in=[status.OBSERVATION, status.OBJECTION])
                .latest("creation_date")
                .expiration_days
            )
        except Exception as _:
            expiration_days = ""

        effective_withdrawal_date = None
        if self.status == status.WITHDRAWN:
            try:
                snapshot_withdrawal_date = (
                    self.snapshots.filter(status=status.WITHDRAWN).latest("creation_date").effective_withdrawal_date
                )
                effective_withdrawal_date = (
                    date_format(snapshot_withdrawal_date, "l j F Y") if snapshot_withdrawal_date else None
                )
            except Exception as _:
                pass
        return {
            "PRODUCT_NAME": self.name,
            "COMPANY_NAME": self.company.social_name if self.company else "",
            "DECLARATION_LINK": self.producer_url,
            "DECLARATION_ID": self.id,
            "EXPIRATION_DAYS": expiration_days,
            "EFFECTIVE_WITHDRAWAL_DATE": effective_withdrawal_date,
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
    def visa_refused(self):
        """
        Vérifie si le dernier refus de visa est effectué après la dernière action du pro.
        """
        from data.models import Snapshot

        user_actions = [
            Snapshot.SnapshotActions.SUBMIT,
            Snapshot.SnapshotActions.RESPOND_TO_OBJECTION,
            Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION,
        ]
        statuses = [
            Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
        ]

        if self.status not in statuses:
            return False

        try:
            latest_visa_refusal = self.snapshots.filter(action=Snapshot.SnapshotActions.REFUSE_VISA).latest(
                "creation_date"
            )
            latest_user_action = self.snapshots.filter(action__in=user_actions).latest("creation_date")
        except Snapshot.DoesNotExist as _:
            return False

        return latest_user_action.creation_date < latest_visa_refusal.creation_date

    @property
    def has_pending_pro_responses(self):
        """
        Vérifie si la déclaration est du côté de l'instruction après au moins un aller-retour avec le pro
        """
        from data.models import Snapshot

        statuses = [
            Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
        ]
        actions = [Snapshot.SnapshotActions.RESPOND_TO_OBJECTION, Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION]

        return self.status in statuses and self.snapshots.filter(action__in=actions).exists()

    @property
    def response_limit_date(self):
        from data.models import Snapshot

        """
        La date limite d'instruction est fixée à deux mois à partir du dernier statut
        "en attente d'instruction" sauf dans le cas d'un refus de visa.

        ⚠️ Attention : Le filtre par date de réponse dans api/views/declaration/declaration.py
        refait la même logique dans la couche DB. Tout changement effectué dans cette fonction
        doit aussi être reflété dans InstructionDateOrderingFilter > filter_queryset.
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
            latest_snapshot = (
                self.snapshots.filter(status=status)
                .exclude(action=Snapshot.SnapshotActions.REFUSE_VISA)
                .latest("creation_date")
            )
            response_limit = latest_snapshot.creation_date + relativedelta(months=2)
            return response_limit
        except Exception as _:
            return None

    def __str__(self):
        return f"Déclaration « {self.name} »"

    @property
    def declared_in_teleicare(self):
        return self.teleicare_declaration_number is not None

    def _has_max_quantity_exceeded(self, substance):
        max_for_target_populations = MaxQuantityPerPopulationRelation.objects.filter(
            population__in=self.populations.all(), substance=substance.substance
        )
        max_for_general_pop = substance.substance.max_quantity
        if max_for_target_populations.exists():
            if substance.quantity > max_for_target_populations.aggregate(Min("max_quantity"))["max_quantity__min"]:
                return True
            # si la déclaration contient des populations qui n'ont pas de dose max renseigné
            if max_for_target_populations.count() < self.populations.count() and max_for_general_pop is not None:
                return substance.quantity > max_for_general_pop
        elif max_for_general_pop is not None:
            # si aucune population cible n'est déclarée
            # OU si aucune max_quantity n'existe pour les populations cibles déclarée
            # => vérifier que la quantité déclarée ne dépasse pas la limite pour la population générale
            if substance.quantity > max_for_general_pop:
                return True

        return False

    def _filter_substances_on_max_quantity_exceeded(self, declared=True):
        """
        Pour chaque substance :
            Si populations cibles définies
                -> vérifier que la plus petite max_quantity pour les populations cibles de la déclaration n'est pas dépassée
            Si aucune population cible définie dans la déclaration ou aucune quantité à ne pas dépasser pour les populations cibles
                -> vérifier que la max_quantity pour la Population générale n'est pas dépassée
        """
        substances = (
            self.declared_substances.exclude(substance__isnull=True).exclude(quantity__isnull=True)
            if declared
            else self.computed_substances.exclude(quantity__isnull=True)
        )
        substances_with_max_quantity_exceeded_ids = []
        for substance in substances:
            if self._has_max_quantity_exceeded(substance):
                substances_with_max_quantity_exceeded_ids.append(substance.id)

        return substances.filter(id__in=substances_with_max_quantity_exceeded_ids)

    @property
    def computed_substances_with_max_quantity_exceeded(self):
        return self._filter_substances_on_max_quantity_exceeded(declared=False)

    @property
    def declared_substances_with_max_quantity_exceeded(self):
        return self._filter_substances_on_max_quantity_exceeded(declared=True)

    @property
    def has_max_quantity_exceeded(self):
        """
        Les doses max sont aujourd'hui définies pour les substances seulement.
        """
        return (
            self.computed_substances_with_max_quantity_exceeded.exists()
            | self.declared_substances_with_max_quantity_exceeded.exists()
        )

    @property
    def risky_ingredients(self):
        return self.declared_ingredients.exclude(new=True).filter(Q(ingredient__is_risky=True))

    @property
    def risky_plants(self):
        # Les plantes ayant public_comments ~* 'la concentration en <nom de substance> est à surveiller' n'impliquent d'obligation règlementaire
        return self.declared_plants.exclude(new=True).filter(
            Q(plant__is_risky=True)
            | Q(plant__name__iregex="dérivés hydroxyanthracéniques|dérivés anthracéniques|HAD")
            | Q(preparation__contains_alcohol=True)
        )

    @property
    def risky_microorganisms(self):
        return self.declared_microorganisms.exclude(new=True).filter(microorganism__is_risky=True)

    @property
    def risky_declared_substances(self):
        return self.declared_substances.exclude(new=True).filter(substance__is_risky=True)

    @property
    def risky_computed_substances(self):
        return self.computed_substances.filter(substance__is_risky=True)

    @property
    def has_risky_ingredients(self):
        return (
            self.risky_ingredients.exists()
            | self.risky_plants.exists()
            | self.risky_microorganisms.exists()
            | self.risky_declared_substances.exists()
            | self.risky_computed_substances.exists()
        )

    @property
    def has_risky_target_population(self):
        """
        Les populations cibles qui sont définies par l'ANSES et utilisées dans les avertissements
        et contre-indications sont considérées comme étant à surveiller avec vigilance lorsqu'utilisées comme population cible
        """
        return any(x for x in self.populations.all() if x.is_defined_by_anses)

    @property
    def acceptation_date(self):
        if self.status == Declaration.DeclarationStatus.AUTHORIZED:
            if self.snapshots.exists():  ## Déclaration complalim
                latest_snapshot = self.snapshots.filter(creation_date__isnull=False).latest("creation_date")
                if latest_snapshot:
                    return latest_snapshot.creation_date
            else:  ## Déclaration Téléicare
                return self.creation_date

    def assign_calculated_article(self):
        """
        Peuple l'article calculé pour cette déclaration.
        La fonction ne sauvegarde pas la déclaration en base. L'appelant doit le faire en cas de besoin.
        Cette décision a été prise pour éviter d'avoir des sauvegardes inutiles.
        Ce sont les particularités des ingrédients et substances contenues dans la composition qui déterminent les articles.
        Dans le cas où plusieurs ingrédients impliqueraient plusieurs articles, certains articles prennent la priorité sur d'autres :
        saisine ANSES (ART_17 et ART_18) > ART_16 > ART_15
        """
        try:
            composition_ingredients = (
                self.declared_plants,
                self.declared_microorganisms,
                self.declared_substances,
                self.computed_substances,
                self.declared_ingredients,
            )
            empty_composition = all(not x.exists() for x in composition_ingredients)
            # cela ne devrait être possible que pour les plantes qui même non autorisées peuvent être ajoutées en infime quantité dans des elixirs

            if empty_composition:
                self.calculated_article = ""
                return

            nutriment_filter = Q(substance__substance_types__contains=[SubstanceType.VITAMIN]) | Q(
                substance__substance_types__contains=[SubstanceType.MINERAL]
            )

            has_overdose_nutriments = (
                self.computed_substances_with_max_quantity_exceeded.filter(nutriment_filter).exists()
                or self.declared_substances_with_max_quantity_exceeded.filter(nutriment_filter).exists()
            )

            if has_overdose_nutriments:
                self.calculated_article = Declaration.Article.ARTICLE_18
                return

            if self.has_max_quantity_exceeded:
                self.calculated_article = Declaration.Article.ANSES_REFERAL
                return

            has_unauthorized_ingredients = (
                any(self.declared_plants.filter(plant__status=IngredientStatus.NOT_AUTHORIZED))
                or any(self.declared_microorganisms.filter(microorganism__status=IngredientStatus.NOT_AUTHORIZED))
                or any(self.declared_substances.filter(substance__status=IngredientStatus.NOT_AUTHORIZED))
                or any(self.declared_ingredients.filter(ingredient__status=IngredientStatus.NOT_AUTHORIZED))
            )

            if has_unauthorized_ingredients:
                self.calculated_article = Declaration.Article.ARTICLE_16
                return

            has_new_ingredients = any(
                x.filter(new=True).exists() for x in composition_ingredients if issubclass(x.model, Addable)
            )

            has_new_plant_parts = any(
                x.filter(is_part_request=True).exclude(request_status=Addable.AddableStatus.REPLACED).exists()
                for x in composition_ingredients
                if issubclass(x.model, DeclaredPlant)
            )

            if has_new_ingredients or has_new_plant_parts:
                self.calculated_article = Declaration.Article.ARTICLE_16
            elif self.has_risky_ingredients or (self.galenic_formulation and self.galenic_formulation.is_risky):
                self.calculated_article = Declaration.Article.ARTICLE_15_WARNING
            elif self.has_risky_target_population:
                self.calculated_article = Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
            else:
                self.calculated_article = Declaration.Article.ARTICLE_15

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

    class AddableStatus(models.TextChoices):
        REQUESTED = "REQUESTED", "Ingrédient ajouté à la déclaration par le déclarant"
        INFORMATION = "INFORMATION", "En attente de plus d'information"
        REJECTED = "REJECTED", "Refusé"
        REPLACED = "REPLACED", "Remplacé par un ingrédient existant"

    new = models.BooleanField(default=False)
    new_description = models.TextField(blank=True, verbose_name="description")

    first_ocurrence = models.BooleanField(
        default=False, verbose_name="Est-ce que cet ingrédient a été rajouté en base suite à cette déclaration ?"
    )

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

    request_status = models.CharField(
        max_length=50,
        choices=AddableStatus.choices,
        default=AddableStatus.REQUESTED,
        verbose_name="statut de la demande de l'ajout du nouvel ingrédient",
    )
    request_private_notes = models.TextField("notes de l'instruction à destination de l'administration", blank=True)

    def clean(self):
        # L'ingrédient ne peut pas être `new` et avoir `first_ocurrence` à true. Le vrai ingrédient
        # doit être référencé dans l'Addable et donc ne pas être nouveau.
        if self.new and self.first_ocurrence:
            raise ValidationError(
                {"first_ocurrence": "Un nouvel ingrédient ne peut pas être le premier à être ajouté en base."}
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
    preparation = models.ForeignKey(
        Preparation, null=True, blank=True, verbose_name="préparation", on_delete=models.RESTRICT
    )
    is_part_request = models.BooleanField(default=False)

    def __str__(self):
        if self.new:
            return f"-NEW- {self.new_name}"
        else:
            return self.plant.name

    @property
    def type(self):
        return "plant"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.plant and self.used_part:
                associated_part = self.plant.plant_parts.through.objects.filter(
                    plant=self.plant, plantpart=self.used_part
                )
                if not associated_part.exists() or associated_part.first().is_useful is False:
                    self.is_part_request = True
        super().save(*args, **kwargs)


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
            return f"-NEW- {self.new_name}"
        return f"{self.microorganism.name}"

    @property
    def type(self):
        return "microorganism"

    @property
    def new_name(self):
        return f"{self.new_species} {self.new_genre}"


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
        if self.new:
            return f"-NEW- {self.new_name}"
        else:
            return self.ingredient.name

    @property
    def type(self):
        return "ingredient"


class DeclaredSubstance(Historisable, Addable):
    class Meta:
        verbose_name = "substance déclarée"
        verbose_name_plural = "substances déclarées"

    declaration = models.ForeignKey(
        Declaration,
        related_name="declared_substances",
        verbose_name=Declaration._meta.verbose_name,
        on_delete=models.CASCADE,
    )
    substance = models.ForeignKey(
        Substance, null=True, blank=True, verbose_name="substance ajoutée par l'user", on_delete=models.RESTRICT
    )
    active = models.BooleanField("ayant une activité physiologique ou nutritionnelle", default=True)
    new_name = models.TextField(blank=True, verbose_name="libellé")
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR")
    unit = models.ForeignKey(SubstanceUnit, null=True, blank=True, verbose_name="unité", on_delete=models.RESTRICT)

    def __str__(self):
        if self.new:
            return f"-NEW- {self.new_name}"
        else:
            return self.substance.name

    @property
    def type(self):
        return "substance"


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
        Substance,
        null=True,
        blank=True,
        verbose_name="substance ajoutée automatiquement car apportée par un ingrédient",
        on_delete=models.RESTRICT,
    )
    quantity = models.FloatField(null=True, blank=True, verbose_name="quantité par DJR")
    unit = models.ForeignKey(SubstanceUnit, null=True, blank=True, verbose_name="unité", on_delete=models.RESTRICT)

    def __str__(self):
        return self.substance.name

    @property
    def type(self):
        return "substance"


# Les pièces jointes peuvent avoir plusieurs types et formats.


class Attachment(Historisable):
    class AttachmentType(models.TextChoices):
        LABEL = "LABEL", "Étiquetage"
        REGULATORY_PROOF = "REGULATORY_PROOF", "Preuve règlementaire"
        CERTIFICATE_AUTHORITY = "CERTIFICATE_AUTHORITY", "Attestation d'une autorité compétente"
        SPEC_SHEET = (
            "SPEC_SHEET",
            "Fiche technique",
        )
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

    class Meta:
        verbose_name = "pièce jointe"
        verbose_name_plural = "pièces jointes"

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

    @property
    def has_pdf_extension(self):
        return self.file and self.file.url.endswith(".pdf")

    @property
    def size(self):
        try:
            return self.file and self.file.size and filesizeformat(self.file.size)
        except Exception as _:
            return ""

    @property
    def extension(self):
        try:
            return self.file and self.file.name and Path(self.file.size).suffix
        except Exception as _:
            return ""

    @property
    def type_display(self):
        return self.get_type_display() or "Type inconnu"
