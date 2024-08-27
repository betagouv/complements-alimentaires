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
    Snapshot,
    Substance,
    SubstanceUnit,
)

from .company import SimpleCompanySerializer
from .ingredient import IngredientSerializer
from .microorganism import MicroorganismSerializer
from .plant import PlantSerializer
from .substance import SubstanceSerializer
from .user import SimpleUserSerializer


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

        # Les nouveaux éléments déclarés seront sauvegardés dans la DB. Ceux déjà présents
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
)


class DeclaredPlantSerializer(serializers.ModelSerializer):
    element = PassthroughPlantSerializer(required=False, source="plant", allow_null=True)
    unit = serializers.PrimaryKeyRelatedField(queryset=SubstanceUnit.objects.all(), required=False, allow_null=True)
    used_part = serializers.PrimaryKeyRelatedField(queryset=PlantPart.objects.all(), required=False, allow_null=True)

    class Meta:
        model = DeclaredPlant
        fields = ADDABLE_ELEMENT_FIELDS + (
            "id",
            "element",
            "new_name",
            "active",
            "used_part",
            "unit",
            "quantity",
            "preparation",
        )

    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        plant = validated_data.pop("plant", None)
        if plant:
            try:
                validated_data["plant"] = Plant.objects.get(pk=plant.get("id"))
            except Plant.DoesNotExist:
                raise ProjectAPIException(field_errors={"declared_plants": "La plante spécifiée n'existe pas."})

        return super().create(validated_data)


class DeclaredMicroorganismSerializer(serializers.ModelSerializer):
    element = PassthroughMicroorganismSerializer(required=False, source="microorganism", allow_null=True)

    class Meta:
        model = DeclaredMicroorganism
        fields = ADDABLE_ELEMENT_FIELDS + (
            "id",
            "element",
            "new_species",
            "new_genre",
            "active",
            "activated",
            "strain",
            "quantity",
        )

    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        microorganism = validated_data.pop("microorganism", None)
        if microorganism:
            try:
                validated_data["microorganism"] = Microorganism.objects.get(pk=microorganism.get("id"))
            except Microorganism.DoesNotExist:
                raise ProjectAPIException(
                    field_errors={"declared_microorganisms": "Le micro-organisme spécifié n'existe pas."}
                )

        return super().create(validated_data)


class DeclaredIngredientSerializer(serializers.ModelSerializer):
    element = PassthroughIngredientSerializer(required=False, source="ingredient", allow_null=True)
    unit = serializers.PrimaryKeyRelatedField(queryset=SubstanceUnit.objects.all(), required=False, allow_null=True)

    class Meta:
        model = DeclaredIngredient
        fields = ADDABLE_ELEMENT_FIELDS + (
            "id",
            "element",
            "new_name",
            "new_type",
            "active",
            "quantity",
            "unit",
        )

    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        ingredient = validated_data.pop("ingredient", None)
        if ingredient:
            try:
                validated_data["ingredient"] = Ingredient.objects.get(pk=ingredient.get("id"))
            except Ingredient.DoesNotExist:
                raise ProjectAPIException(field_errors={"declared_ingredients": "L'ingrédient spécifié n'existe pas."})

        return super().create(validated_data)


class DeclaredSubstanceSerializer(serializers.ModelSerializer):
    element = PassthroughSubstanceSerializer(required=False, source="substance", allow_null=True)

    class Meta:
        model = DeclaredSubstance
        fields = (
            "id",
            "element",
            "active",
        )

    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        substance = validated_data.pop("substance", None)
        if substance:
            try:
                validated_data["substance"] = Substance.objects.get(pk=substance.get("id"))
            except Substance.DoesNotExist:
                raise ProjectAPIException(field_errors={"declared_substances": "La substance spécifiée n'existe pas."})

        return super().create(validated_data)


class ComputedSubstanceSerializer(serializers.ModelSerializer):
    substance = PassthroughSubstanceSerializer()
    unit = serializers.PrimaryKeyRelatedField(queryset=SubstanceUnit.objects.all(), required=False, allow_null=True)

    class Meta:
        model = ComputedSubstance
        fields = (
            "id",
            "substance",
            "quantity",
            "unit",
        )

    def create(self, validated_data):
        # DRF ne gère pas automatiquement la création des nested-fields :
        # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        substance = validated_data.pop("substance", None)
        if substance:
            try:
                validated_data["substance"] = Substance.objects.get(pk=substance.get("id"))
            except Substance.DoesNotExist:
                raise ProjectAPIException(field_errors={"declared_substances": "La substance spécifiée n'existe pas."})

        return super().create(validated_data)


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

    class Meta:
        model = Declaration
        fields = (
            "id",
            "status",
            "author",
            "company",
            "name",
            "brand",
            "gamme",
            "description",
            "modification_date",
            "creation_date",
            "instructor",
            "visor",
            "response_limit_date",
        )
        read_only_fields = fields


class DeclarationSerializer(serializers.ModelSerializer):
    instructor = SimpleUserSerializer(read_only=True, source="instructor.user")
    visor = SimpleUserSerializer(read_only=True, source="visor.user")
    author = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), allow_null=True)
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
    blocking_reasons = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Declaration
        fields = (
            "id",
            "status",
            "author",
            "company",
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
            "private_notes",
            "blocking_reasons",
            "expiration_date",
        )
        read_only_fields = (
            "id",
            "status",
            "author",
            "instructor",
            "visor",
            "post_validation_status",
            "post_validation_producer_message",
            "post_validation_expiration_days",
            "private_notes",
        )

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

    def to_representation(self, obj):
        """
        On surcharge cette méthode pour assurer que les notes privées ne soient pas
        sérialisées si la personne ne fait pas partie de l'administration
        """
        ret = super().to_representation(obj)
        request = self.context.get("request")
        view = self.context.get("view")
        can_see_private_notes = (
            request
            and view
            and (IsVisor().has_permission(request, view) or IsInstructor().has_permission(request, view))
        )

        if not can_see_private_notes:
            ret.pop("private_notes")
        return ret

    def get_blocking_reasons(self, obj):
        try:
            latest_snapshot = obj.snapshots.filter(blocking_reasons__isnull=False).latest("creation_date")
            return latest_snapshot.blocking_reasons
        except Snapshot.DoesNotExist:
            return None


class DeclarationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = (
            "id",
            "status",
            "author",
            "company",
            "name",
            "brand",
            "gamme",
            "flavor",
            "description",
            "creation_date",
            "modification_date",
        )
        read_only_fields = fields
