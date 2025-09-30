from rest_framework import serializers

from data.models import Ingredient, IngredientSynonym

from .common_ingredient import (
    COMMON_FETCH_FIELDS,
    COMMON_FIELDS,
    COMMON_NAME_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
    WithSubstances,
)
from .substance import SubstanceShortSerializer


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
            "description",
            "substances",
        )
        read_only_fields = fields


class IngredientSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientSynonym
        fields = (
            "name",
            "synonym_type",
        )


class IngredientModificationSerializer(CommonIngredientModificationSerializer, WithSubstances):
    synonyms = IngredientSynonymModificationSerializer(many=True, source="ingredientsynonym_set", required=False)

    synonym_model = IngredientSynonym
    synonym_set_field_name = "ingredientsynonym_set"

    declaredingredient_set_field_names = ["declaredingredient_set"]

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
