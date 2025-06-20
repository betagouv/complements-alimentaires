from drf_base64.fields import Base64FileField
from openpyxl.cell.cell import Hyperlink
from rest_framework import serializers

from api.exceptions import ProjectAPIException
from api.permissions import IsInstructor, IsVisor
from api.utils.urls import get_base_url
from data.models import (
    Attachment,
    Company,
    ComputedSubstance,
    Condition,
    Declaration,
    DeclaredIngredient,
    DeclaredMicroorganism,
    DeclaredPlant,
    DeclaredSubstance,
    Effect,
    Ingredient,
    Microorganism,
    Plant,
    PlantPart,
    Population,
    Substance,
    SubstanceUnit,
)

from .company import MinimalCompanySerializer, SimpleCompanySerializer
from .ingredient import IngredientSerializer
from .microorganism import MicroorganismSerializer
from .plant import PlantSerializer
from .substance import SubstanceSerializer
from .user import SimpleUserSerializer
from .utils import PrivateFieldsSerializer


class IdPassthrough:
    """
    Permet de passer l'ID des nested-objects dans les serializers
    """

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields["id"].read_only = False


class PassthroughPlantSerializer(IdPassthrough, PlantSerializer):
    pass


class PassthroughMicroorganismSerializer(IdPassthrough, MicroorganismSerializer):
    pass


class PassthroughIngredientSerializer(IdPassthrough, IngredientSerializer):
    pass


class PassthroughSubstanceSerializer(IdPassthrough, SubstanceSerializer):
    pass


class DeclaredListSerializer(serializers.ListSerializer):
    """
    Pour les modèles liés et les list serializers on a besoin de spécifier le comportement
    dans une mise à jour car DRF ne peut pas le deviner:
    https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-update
    """

    def update(self, instance, validated_data):
        instance_mapping = {element.id: element for element in instance}

        declared_items = []

        # Les nouveaux ingrédients déclarés seront sauvegardés dans la DB. Ceux déjà présents
        # seront mis à jour.
        for item in validated_data:
            element = instance_mapping.get(item.get("id"), None)
            if element is None:
                declared_items.append(self.child.create(item))
            else:
                declared_items.append(self.child.update(element, item))

        # Si des instances des éléments déclarés sont enlevés, ils seront aussi supprimés
        # de la base
        data_mapping = {item["id"]: item for item in validated_data if item.get("id")}
        for element_id, element in instance_mapping.items():
            if element_id not in data_mapping:
                element.delete()

        return declared_items


ADDABLE_ELEMENT_FIELDS = (
    "new",
    "new_name",
    "new_description",
    "authorization_mode",
    "fr_reason",
    "fr_details",
    "eu_reference_country",
    "eu_legal_source",
    "eu_details",
    "request_status",
    "request_private_notes",
)

DECLARED_ELEMENT_SHARED_FIELDS = ADDABLE_ELEMENT_FIELDS + ("type",)


class DeclaredElementNestedField:
    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    def create(self, validated_data):
        self._set_element(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._set_element(validated_data)
        return super().update(instance, validated_data)

    def _set_element(self, validated_data):
        element = validated_data.pop(self.nested_field_name, None)
        if element:
            id = element.get("id")
            try:
                validated_data[self.nested_field_name] = self.nested_model.objects.get(pk=id)
            except self.nested_model.DoesNotExist:
                raise ProjectAPIException(
                    field_errors={
                        f"declared_{self.nested_field_name}s": f"L'ingrédient avec l'id « {id} » spécifiée n'existe pas."
                    }
                )


class DeclaredIngredientCommonSerializer(DeclaredElementNestedField, PrivateFieldsSerializer):
    private_fields = ("request_private_notes", "request_status")


class DeclaredPlantSerializer(DeclaredIngredientCommonSerializer):
    element = PassthroughPlantSerializer(required=False, source="plant", allow_null=True)
    unit = serializers.PrimaryKeyRelatedField(queryset=SubstanceUnit.objects.all(), required=False, allow_null=True)
    used_part = serializers.PrimaryKeyRelatedField(queryset=PlantPart.objects.all(), required=False, allow_null=True)
    declaration = serializers.PrimaryKeyRelatedField(read_only=True)

    nested_field_name = "plant"
    nested_model = Plant

    class Meta:
        model = DeclaredPlant
        fields = DECLARED_ELEMENT_SHARED_FIELDS + (
            "id",
            "declaration",
            "element",
            "active",
            "used_part",
            "quantity",
            "unit",
            "preparation",
        )


class DeclaredMicroorganismSerializer(DeclaredIngredientCommonSerializer):
    element = PassthroughMicroorganismSerializer(required=False, source="microorganism", allow_null=True)
    declaration = serializers.PrimaryKeyRelatedField(read_only=True)

    nested_field_name = "microorganism"
    nested_model = Microorganism

    class Meta:
        model = DeclaredMicroorganism
        fields = DECLARED_ELEMENT_SHARED_FIELDS + (
            "id",
            "declaration",
            "element",
            "active",
            "activated",
            "new_species",
            "new_genre",
            "strain",
            "quantity",
        )


class DeclaredIngredientSerializer(DeclaredIngredientCommonSerializer):
    element = PassthroughIngredientSerializer(required=False, source="ingredient", allow_null=True)
    unit = serializers.PrimaryKeyRelatedField(queryset=SubstanceUnit.objects.all(), required=False, allow_null=True)
    declaration = serializers.PrimaryKeyRelatedField(read_only=True)

    nested_field_name = "ingredient"
    nested_model = Ingredient

    class Meta:
        model = DeclaredIngredient
        fields = DECLARED_ELEMENT_SHARED_FIELDS + (
            "id",
            "declaration",
            "element",
            "active",
            "new_type",
            "quantity",
            "unit",
        )


class DeclaredSubstanceSerializer(DeclaredIngredientCommonSerializer):
    element = PassthroughSubstanceSerializer(required=False, source="substance", allow_null=True)
    declaration = serializers.PrimaryKeyRelatedField(read_only=True)

    nested_field_name = "substance"
    nested_model = Substance

    class Meta:
        model = DeclaredSubstance
        fields = DECLARED_ELEMENT_SHARED_FIELDS + (
            "id",
            "declaration",
            "element",
            "active",
            "quantity",
            "unit",
        )


class ComputedSubstanceSerializer(DeclaredElementNestedField, serializers.ModelSerializer):
    substance = PassthroughSubstanceSerializer()
    unit = serializers.PrimaryKeyRelatedField(queryset=SubstanceUnit.objects.all(), required=False, allow_null=True)

    nested_field_name = "substance"
    nested_model = Substance

    class Meta:
        model = ComputedSubstance
        fields = (
            "id",
            "substance",
            "quantity",
            "unit",
        )


class AttachmentSerializer(IdPassthrough, serializers.ModelSerializer):
    file = Base64FileField()

    class Meta:
        model = Attachment
        fields = (
            "id",
            "file",
            "type",
            "type_display",
            "name",
            "size",
        )
        read_only_fields = ("file",)

    def validate_file(self, file):
        size_limit = 1048576 * 2
        if file.size > size_limit:
            raise ProjectAPIException(
                field_errors=[{"attachments": "La pièce jointe dépasse la taille limite de 2 Mo"}]
            )
        return file


class SimpleDeclarationSerializer(serializers.ModelSerializer):
    instructor = SimpleUserSerializer(read_only=True, source="instructor.user")
    visor = SimpleUserSerializer(read_only=True, source="visor.user")
    author = SimpleUserSerializer(read_only=True)
    company = SimpleCompanySerializer(read_only=True)
    mandated_company = SimpleCompanySerializer(read_only=True)
    unit_measurement = serializers.PrimaryKeyRelatedField(
        queryset=SubstanceUnit.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Declaration
        fields = (
            "id",
            "teleicare_declaration_number",
            "siccrf_id",
            "status",
            "author",
            "company",
            "mandated_company",
            "name",
            "brand",
            "gamme",
            "description",
            "modification_date",
            "creation_date",
            "instructor",
            "visor",
            "response_limit_date",
            "visa_refused",
            "has_pending_pro_responses",
            "article",
            "unit_quantity",
            "unit_measurement",
        )
        read_only_fields = fields


class ExcelExportDeclarationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(read_only=True, source="company.social_name")
    siret = serializers.CharField(read_only=True, source="company.siret")
    vat = serializers.CharField(read_only=True, source="company.vat")
    article = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    department = serializers.CharField(read_only=True, source="company.department")

    # Champ spécial utilisé par drf-excel documenté ici : https://github.com/django-commons/drf-excel
    row_color = serializers.SerializerMethodField()

    class Meta:
        model = Declaration
        fields = (
            "name",
            "brand",
            "article",
            "status",
            "company_name",
            "siret",
            "vat",
            "department",
            "row_color",  # Champ utilisé en interne par drf-excel
        )
        read_only_fields = fields

    def get_row_color(self, instance):
        """
        Permet d'alterner les couleurs des files dans le ficher Excel
        """
        return ["FFFFFFFF", "FFECECFE"][(*self.instance,).index(instance) % 2]

    def get_status(self, instance):
        return instance.get_status_display()

    def get_article(self, instance):
        return Declaration.Article(instance.article).label if instance.article else None

    def to_representation(self, instance):
        """
        Hack pour ajouter un lien dans le `DeclarationHyperlinkXLSXRenderer`.
        Ce bug a été levé côté dfr-excel : https://github.com/django-commons/drf-excel/issues/112
        Le champ `url_field` ne sera pas présent dans le tableau Excel, mais servirà à
        programmatiquement ajouter le lien dans le nom du produit.
        """

        data = super().to_representation(instance)
        data["url_field"] = Hyperlink(ref=f"{get_base_url()}recherche-avancee/{instance.id}", display=instance.name)
        return data


def add_enum_or_personnalized_value(item, custom_value):
    if item:
        if "(à préciser)" not in str(item).lower():
            return item.name
        else:
            return "Autre : " + str(custom_value)


class OpenDataDeclarationSerializer(serializers.ModelSerializer):
    teleicare_id = serializers.IntegerField(source="siccrf_id")
    numero_declaration_teleicare = serializers.CharField(
        allow_blank=True, required=False, source="teleicare_declaration_number"
    )
    decision = serializers.SerializerMethodField()
    date_decision = serializers.DateTimeField(required=False, source="acceptation_date")
    responsable_mise_sur_marche = serializers.SerializerMethodField()
    siret_responsable_mise_sur_marche = serializers.SerializerMethodField()
    vat_responsable_mise_sur_marche = serializers.SerializerMethodField()
    nom_commercial = serializers.SerializerMethodField()
    marque = serializers.CharField(allow_blank=True, required=False, source="brand")
    article_procedure = serializers.SerializerMethodField()
    forme_galenique = serializers.SerializerMethodField()
    dose_journaliere = serializers.CharField(allow_blank=True, required=False, source="daily_recommended_dose")
    mode_emploi = serializers.CharField(allow_blank=True, required=False, source="instructions")
    mises_en_garde = serializers.CharField(allow_blank=True, required=False, source="warning")
    objectif_effet = serializers.SerializerMethodField()
    aromes = serializers.CharField(allow_blank=True, required=False, source="flavor")
    facteurs_risques = serializers.SerializerMethodField()
    populations_cibles = serializers.SerializerMethodField()
    plantes = serializers.SerializerMethodField()
    micro_organismes = serializers.SerializerMethodField()
    substances = serializers.SerializerMethodField()
    additifs = serializers.SerializerMethodField()
    nutriments = serializers.SerializerMethodField()
    autres_ingredients_actifs = serializers.SerializerMethodField()
    ingredients_inactifs = serializers.SerializerMethodField()

    class Meta:
        model = Declaration

        fields = (
            "id",
            "teleicare_id",
            "numero_declaration_teleicare",
            "decision",
            "responsable_mise_sur_marche",
            "adresse_responsable_mise_sur_marche",
            "siret_responsable_mise_sur_marche",
            "vat_responsable_mise_sur_marche",
            "nom_commercial",
            "marque",
            "gamme",
            "article_procedure",
            "forme_galenique",
            "dose_journaliere",
            "mode_emploi",
            "mises_en_garde",
            "objectif_effet",
            "aromes",
            "facteurs_risques",
            "populations_cibles",
            "plantes",
            "micro_organismes",
            "substances",
            "additifs",
            "nutriments",
            "autres_ingredients_actifs",
            "ingredients_inactifs",
            "date_decision",
        )
        read_only_fields = fields

    def get_decision(self, obj):
        return obj.get_status_display()

    def get_responsable_mise_sur_marche(self, obj):
        return obj.company.commercial_name

    def get_adresse_responsable_mise_sur_marche(self, obj):
        return {
            "code_postal": obj.company.postal_code,
            "pays": obj.company.country,
        }

    def get_siret_responsable_mise_sur_marche(self, obj):
        return obj.company.siret

    def get_vat_responsable_mise_sur_marche(self, obj):
        return obj.company.vat

    def get_nom_commercial(self, obj):
        return obj.name

    def get_article_procedure(self, obj):
        """
        Unifie tous les types d'Articles 15.
        Si ce n'est pas un Article 15, alors le display name est retourné
        """
        if obj.article in [
            Declaration.Article.ARTICLE_15,
            Declaration.Article.ARTICLE_15_WARNING,
            Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION,
        ]:
            return "Article 15"
        elif obj.article:
            return Declaration.Article(obj.article).label

    def get_forme_galenique(self, obj):
        return add_enum_or_personnalized_value(obj.galenic_formulation, obj.other_galenic_formulation)

    def get_objectif_effet(self, obj):
        effects = []
        for effect in obj.effects.all():
            effects.append(add_enum_or_personnalized_value(effect, obj.other_effects))
        return effects

    def get_facteurs_risques(self, obj):
        risk_factors = []
        for risk_factor in obj.conditions_not_recommended.all():
            risk_factors.append(add_enum_or_personnalized_value(risk_factor, obj.other_effects))
        return risk_factors

    def get_populations_cibles(self, obj):
        return [population.name for population in obj.populations.all()]

    def get_plantes(self, obj):
        return [
            {
                "nom": declared_plant.plant.name if declared_plant.plant else None,
                "partie": declared_plant.used_part.name if declared_plant.used_part else None,
                "preparation": declared_plant.preparation.name if declared_plant.preparation else None,
                "quantité_par_djr": declared_plant.quantity if declared_plant.quantity else None,
                "unite": declared_plant.unit.name,
            }
            if declared_plant.unit
            else {}
            for declared_plant in obj.declared_plants.filter(active=True)
        ]

    def get_micro_organismes(self, obj):
        return [
            {
                "genre": declared_microorganism.microorganism.genus if declared_microorganism.microorganism else None,
                "espece": declared_microorganism.microorganism.species
                if declared_microorganism.microorganism
                else None,
                "souche": declared_microorganism.strain
                if declared_microorganism.strain
                else None,  # elle est normalement obligatoire mais quelques entrées ont pu être rentrées avant le required
                "quantité_par_djr": declared_microorganism.quantity if declared_microorganism.activated else None,
                "inactive": not declared_microorganism.activated,
            }
            for declared_microorganism in obj.declared_microorganisms.all()
        ]

    def get_substances(self, obj):
        return [
            {
                "nom": declared_substance.substance.name,
                "quantité_par_djr": declared_substance.quantity,
                "unite": declared_substance.unit.name,
            }
            if declared_substance.substance and declared_substance.quantity and declared_substance.unit
            else {}
            for declared_substance in obj.declared_substances.all()
        ]

    def get_additifs(self, obj):
        return [
            str(declared_ingredient.ingredient.name)
            for declared_ingredient in obj.declared_ingredients.filter(ingredient__ingredient_type=2)
        ]

    def get_nutriments(self, obj):
        return [
            str(declared_ingredient.ingredient.name)
            for declared_ingredient in obj.declared_ingredients.filter(ingredient__ingredient_type=1)
        ]

    def get_autres_ingredients_actifs(self, obj):
        return [
            str(declared_ingredient.ingredient.name)
            for declared_ingredient in obj.declared_ingredients.filter(ingredient__ingredient_type=4)
        ]

    def get_ingredients_inactifs(self, obj):
        return [
            str(declared_ingredient.ingredient.name)
            for declared_ingredient in obj.declared_ingredients.filter(ingredient__ingredient_type=5)
        ]


class DeclarationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get("context", {})
        request = context.get("request")
        view = context.get("view")
        if not request or not view:
            return

        is_instructor = IsInstructor().has_permission(request, view)
        is_visor = IsVisor().has_permission(request, view)
        if not is_instructor and not is_visor:
            self.fields.pop("private_notes_instruction")
            self.fields.pop("private_notes_visa")
        else:
            self.fields["private_notes_instruction"].read_only = not is_instructor
            self.fields["private_notes_visa"].read_only = not is_visor

    instructor = SimpleUserSerializer(read_only=True, source="instructor.user")
    visor = SimpleUserSerializer(read_only=True, source="visor.user")
    author = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), allow_null=True)
    mandated_company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), allow_null=True, required=False
    )
    unit_measurement = serializers.PrimaryKeyRelatedField(
        queryset=SubstanceUnit.objects.all(), required=False, allow_null=True
    )
    conditions_not_recommended = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Condition.objects.all(), required=False, allow_null=True
    )
    populations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Population.objects.all(), required=False, allow_null=True
    )
    effects = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Effect.objects.all(), required=False, allow_null=True
    )

    declared_plants = DeclaredListSerializer(child=DeclaredPlantSerializer(), required=False)
    declared_microorganisms = DeclaredListSerializer(child=DeclaredMicroorganismSerializer(), required=False)
    declared_ingredients = DeclaredListSerializer(child=DeclaredIngredientSerializer(), required=False)
    declared_substances = DeclaredListSerializer(child=DeclaredSubstanceSerializer(), required=False)
    computed_substances = DeclaredListSerializer(child=ComputedSubstanceSerializer(), required=False)
    declared_substances_with_max_quantity_exceeded = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    computed_substances_with_max_quantity_exceeded = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    attachments = DeclaredListSerializer(child=AttachmentSerializer(), required=False)
    name = serializers.CharField(allow_blank=False, required=True)
    private_notes_instruction = serializers.CharField(allow_blank=True, required=False)
    private_notes_visa = serializers.CharField(allow_blank=True, required=False)
    blocking_reasons = serializers.ListField(read_only=True)

    class Meta:
        model = Declaration
        fields = (
            "id",
            "teleicare_declaration_number",
            "siccrf_id",
            "article",
            "status",
            "author",
            "company",
            "mandated_company",
            "address",
            "additional_details",
            "postal_code",
            "city",
            "cedex",
            "country",
            "name",
            "brand",
            "gamme",
            "flavor",
            "description",
            "galenic_formulation",
            "unit_quantity",
            "unit_measurement",
            "conditioning",
            "daily_recommended_dose",
            "minimum_duration",
            "instructions",
            "warning",
            "populations",
            "conditions_not_recommended",
            "effects",
            "declared_plants",
            "declared_microorganisms",
            "declared_ingredients",
            "declared_substances",
            "computed_substances",
            "has_max_quantity_exceeded",
            "declared_substances_with_max_quantity_exceeded",
            "computed_substances_with_max_quantity_exceeded",
            "attachments",
            "other_effects",
            "other_galenic_formulation",
            "other_conditions",
            "instructor",
            "visor",
            "post_validation_status",
            "post_validation_producer_message",
            "post_validation_expiration_days",
            "private_notes_instruction",
            "private_notes_visa",
            "blocking_reasons",
            "expiration_date",
            "last_administration_comment",
        )
        read_only_fields = (
            "id",
            "article",
            "status",
            "author",
            "instructor",
            "visor",
            "post_validation_status",
            "post_validation_producer_message",
            "post_validation_expiration_days",
            "private_notes_instruction",
            "private_notes_visa",
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """
        Pre-chargement des données nécessaires pour éviter des soucis de prod
        http://ses4j.github.io/2015/11/23/optimizing-slow-django-rest-framework-performance/
        """
        queryset = queryset.select_related(
            "author",
            "company",
            "mandated_company",
            "unit_measurement",
            "galenic_formulation",
        )

        queryset = queryset.prefetch_related(
            "declared_plants__plant__substances",
            "declared_plants__plant",
            "declared_plants__preparation",
            "declared_plants__unit",
            "declared_microorganisms__microorganism__substances",
            "declared_ingredients__ingredient__substances",
            "declared_substances__substance",
            "declared_substances__unit",
            "computed_substances__substance",
            "computed_substances__unit",
            "attachments",
        )
        return queryset

    @property
    def should_calculate_article(self):
        """
        Pour ne pas calculer l'article à chaque changement, nous le calculons seulement si
        le queryparam force-article-calculation=true est présent dans l'URL de la requête
        """
        request = self.context.get("request")
        return request and request.query_params.get("force-article-calculation", "").lower() == "true"

    def calculate_article(self, declaration):
        declaration.refresh_from_db()  # Besoin de ce refresh pour prendre en compte les changements sur la compo
        declaration.assign_calculated_article()
        declaration.save()
        declaration.refresh_from_db()  # Besoin de ce refresh pour le generated field "article"

    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        if self.context.get("request"):
            validated_data["author"] = self.context.get("request").user

        declaration = self._assign_declared_items(None, validated_data)
        if self.should_calculate_article:
            self.calculate_article(declaration)
        return declaration

    def update(self, instance, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        declaration = self._assign_declared_items(instance, validated_data)
        if self.should_calculate_article:
            self.calculate_article(declaration)
        return declaration

    def _assign_declared_items(self, instance, validated_data):
        """
        Enlève les éléments déclarés pour les traiter manuellement, en leur assignant la déclaration
        et en les mettant dans la base de données.
        """
        declared_fields = [
            "declared_plants",
            "declared_microorganisms",
            "declared_ingredients",
            "declared_substances",
            "computed_substances",
            "attachments",
        ]
        declared_data = [(field, validated_data.pop(field, None)) for field in declared_fields]

        declaration = super().update(instance, validated_data) if instance else super().create(validated_data)

        for field_name, declared_elements in declared_data:
            if declared_elements is not None:
                serializer = self.fields[field_name]
                for item in declared_elements:
                    item["declaration"] = declaration
                if instance:
                    serializer.update(getattr(declaration, field_name).all(), declared_elements)
                else:
                    serializer.create(declared_elements)

        return declaration


class DeclarationShortSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    company = SimpleCompanySerializer(read_only=True)
    mandated_company = SimpleCompanySerializer(read_only=True)

    class Meta:
        model = Declaration
        fields = (
            "id",
            "teleicare_declaration_number",
            "siccrf_id",
            "status",
            "author",
            "company",
            "mandated_company",
            "name",
            "brand",
            "gamme",
            "flavor",
            "description",
            "creation_date",
            "modification_date",
        )
        read_only_fields = fields


class DeclaredElementDeclarationSerializer(serializers.ModelSerializer):
    company = MinimalCompanySerializer(read_only=True)

    class Meta:
        model = Declaration
        fields = ("id", "status", "author", "company", "name", "response_limit_date")
        read_only_fields = fields


class DeclaredElementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    type = serializers.CharField()
    authorization_mode = serializers.CharField()
    declaration = DeclaredElementDeclarationSerializer()
    request_status = serializers.CharField()

    def get_name(self, obj):
        return str(obj)
