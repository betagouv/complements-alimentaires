from rest_framework import serializers
from data.models import Ingredient, IngredientSynonym
from .substance import SubstanceShortSerializer


class IngredientSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class IngredientSerializer(serializers.ModelSerializer):
    synonyms = IngredientSynonymSerializer(many=True, read_only=True, source="ingredientsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "name_en",
            "observation",
            "description",
            "synonyms",
            "substances",
        )
        read_only_fields = fields
