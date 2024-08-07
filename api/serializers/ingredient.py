from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import Ingredient, IngredientStatus, IngredientSynonym

from .historical_record import HistoricalRecordField
from .substance import SubstanceShortSerializer
from .utils import PrivateCommentSerializer


class IngredientSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class IngredientSerializer(PrivateCommentSerializer):
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
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "activity",
            "status",
            "history",
            "object_type",
        )
        read_only_fields = fields
