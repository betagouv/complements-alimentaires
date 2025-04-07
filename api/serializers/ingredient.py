from rest_framework import serializers

from data.models import Ingredient, IngredientSynonym

from .substance import SubstanceShortSerializer
from .common_ingredient import (
    COMMON_FIELDS,
    COMMON_NAME_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    COMMON_FETCH_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
    WithSubstances,
    WithName,
)


class IngredientSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class IngredientSerializer(CommonIngredientReadSerializer):
    synonyms = IngredientSynonymSerializer(many=True, read_only=True, source="ingredientsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = COMMON_FETCH_FIELDS + (
            "name_en",
            "description",
            "substances",
        )
        read_only_fields = fields


class IngredientSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientSynonym
        fields = ("name",)


class IngredientModificationSerializer(CommonIngredientModificationSerializer, WithSubstances, WithName):
    synonyms = IngredientSynonymModificationSerializer(many=True, source="ingredientsynonym_set", required=False)

    synonym_model = IngredientSynonym
    synonym_set_field_name = "ingredientsynonym_set"

    class Meta:
        model = Ingredient
        fields = (
            COMMON_FIELDS
            + COMMON_NAME_FIELDS
            + (
                "ingredient_type",
                "substances",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS
