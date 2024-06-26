from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import Ingredient, IngredientStatus, IngredientSynonym

from .historical_record import HistoricalRecordField
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
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "name_en",
            "description",
            "synonyms",
            "substances",
            "public_comments",
            "status",
            "history",
            "object_type",
        )
        read_only_fields = fields
