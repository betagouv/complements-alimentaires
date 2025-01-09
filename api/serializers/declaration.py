from drf_base64.fields import Base64FileField
from rest_framework import serializers

from api.exceptions import ProjectAPIException
from api.permissions import IsInstructor, IsVisor
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

from .company import SimpleCompanySerializer
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
    dans une mise à jour car DRF ne peut pas le déviner:
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
    "authorization_mode",
    "fr_reason",
    "fr_details",
    "eu_reference_country",
    "eu_legal_source",
    "eu_details",
    "new_description",
    "new",
    "request_private_notes",
    "request_status",
)


class DeclaredElementNestedField:
    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
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

        return super().create(validated_data)


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
        fields = ADDABLE_ELEMENT_FIELDS + (
            "id",
            "declaration",
            "element",
            "new_name",
            "active",
            "used_part",
            "unit",
            "quantity",
            "preparation",
            "type",
        )


class DeclaredMicroorganismSerializer(DeclaredIngredientCommonSerializer):
    element = PassthroughMicroorganismSerializer(required=False, source="microorganism", allow_null=True)
    declaration = serializers.PrimaryKeyRelatedField(read_only=True)

    nested_field_name = "microorganism"
    nested_model = Microorganism

    class Meta:
        model = DeclaredMicroorganism
        fields = ADDABLE_ELEMENT_FIELDS + (
            "id",
            "declaration",
            "element",
            "new_species",
            "new_genre",
            "active",
            "activated",
            "strain",
            "quantity",
            "type",
        )


class DeclaredIngredientSerializer(DeclaredIngredientCommonSerializer):
    element = PassthroughIngredientSerializer(required=False, source="ingredient", allow_null=True)
    unit = serializers.PrimaryKeyRelatedField(queryset=SubstanceUnit.objects.all(), required=False, allow_null=True)
    declaration = serializers.PrimaryKeyRelatedField(read_only=True)

    nested_field_name = "ingredient"
    nested_model = Ingredient

    class Meta:
        model = DeclaredIngredient
        fields = ADDABLE_ELEMENT_FIELDS + (
            "id",
            "declaration",
            "element",
            "new_name",
            "new_type",
            "active",
            "quantity",
            "unit",
            "type",
        )


class DeclaredSubstanceSerializer(DeclaredIngredientCommonSerializer):
    element = PassthroughSubstanceSerializer(required=False, source="substance", allow_null=True)
    declaration = serializers.PrimaryKeyRelatedField(read_only=True)

    nested_field_name = "substance"
    nested_model = Substance

    class Meta:
        model = DeclaredSubstance
        fields = ADDABLE_ELEMENT_FIELDS + (
            "id",
            "declaration",
            "element",
            "new_name",
            "active",
            "quantity",
            "unit",
            "type",
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
    file = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = Attachment
        fields = (
            "id",
            "file",
            "type",
            "name",
        )
        read_only_fields = ("file",)

    def validate_file(self, file):
        if not file:
            return None

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

    class Meta:
        model = Declaration
        fields = (
            "id",
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
        )
        read_only_fields = fields


class OpenDataDeclarationSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    galenic_formulation = serializers.SerializerMethodField()
    effects = serializers.SerializerMethodField()
    conditions_not_recommended = serializers.SerializerMethodField()

    populations = serializers.SerializerMethodField()

    declared_plants = serializers.SerializerMethodField()
    declared_microorganisms = serializers.SerializerMethodField()
    declared_substances = serializers.SerializerMethodField()
    declared_additives = serializers.SerializerMethodField()
    declared_nutriments = serializers.SerializerMethodField()
    declared_other_active_ingredients = serializers.SerializerMethodField()

    modification_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Declaration
        fields = (
            "id",
            "status",
            "company",
            "name",
            "brand",
            "gamme",
            "article",
            "galenic_formulation",
            "daily_recommended_dose",
            "instructions",
            "warning",
            "effects",
            "flavor",
            "conditions_not_recommended",
            "populations",
            "declared_plants",
            "declared_microorganisms",
            "declared_substances",
            "declared_additives",
            "declared_nutriments",
            "declared_other_active_ingredients",
            "modification_date",
        )
        read_only_fields = fields

    def get_status(self, obj):
        return obj.get_status_display()

    def get_article(self, obj):
        """
        Unify all types of Articles 15 categories.
        If not part of Article 15, then return display name
        """
        if "ART_15" in obj.get_calculated_article_display():
            return "ART_15"
        else:
            return obj.get_calculated_article_display()

    def get_company(self, obj):
        return obj.company.commercial_name, obj.company.siret

    def get_galenic_formulation(self, obj):
        if obj.galenic_formulation:
            return obj.galenic_formulation.name
        else:
            return None

    def get_effects(self, obj):
        return [effect.name for effect in obj.effects.all()]

    def get_conditions_not_recommended(self, obj):
        return [condition.name for condition in obj.conditions_not_recommended.all()]

    def get_populations(self, obj):
        return [population.name for population in obj.populations.all()]

    def get_declared_plants(self, obj):
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

    def get_declared_microorganisms(self, obj):
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

    def get_declared_substances(self, obj):
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

    def get_declared_additives(self, obj):
        return [
            str(declared_ingredient.ingredient.name)
            for declared_ingredient in obj.declared_ingredients.filter(ingredient__ingredient_type=2)
        ]

    def get_declared_nutriments(self, obj):
        return [
            str(declared_ingredient.ingredient.name)
            for declared_ingredient in obj.declared_ingredients.filter(ingredient__ingredient_type=1)
        ]

    def get_declared_other_active_ingredients(self, obj):
        return [
            str(declared_ingredient.ingredient.name)
            for declared_ingredient in obj.declared_ingredients.filter(ingredient__ingredient_type=4)
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
    attachments = DeclaredListSerializer(child=AttachmentSerializer(), required=False)
    name = serializers.CharField(allow_blank=False, required=True)
    private_notes_instruction = serializers.CharField(allow_blank=True, required=False)
    private_notes_visa = serializers.CharField(allow_blank=True, required=False)
    blocking_reasons = serializers.ListField(read_only=True)

    class Meta:
        model = Declaration
        fields = (
            "id",
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
            "declared_microorganisms__microorganism__substances",
            "declared_ingredients__ingredient__substances",
            "declared_substances__substance",
            "computed_substances__substance",
            "attachments",
        )
        return queryset

    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        if self.context.get("request"):
            validated_data["author"] = self.context.get("request").user

        return self._assign_declared_items(None, validated_data)

    def update(self, instance, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        return self._assign_declared_items(instance, validated_data)

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


class DeclaredElementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    type = serializers.CharField()
    authorization_mode = serializers.CharField()
    declaration = DeclarationShortSerializer()

    def get_name(self, obj):
        return str(obj)
