from rest_framework import serializers
from data.models import Microorganism, MicroorganismSynonym, IngredientStatus
from api.utils.choice_field import GoodReprChoiceField

from .substance import SubstanceShortSerializer


class MicroorganismSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroorganismSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class MicroorganismSerializer(serializers.ModelSerializer):
    synonyms = MicroorganismSynonymSerializer(many=True, read_only=True, source="microorganismsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)

    class Meta:
        model = Microorganism
        fields = (
            "id",
            "name",
            "genus",
            "species",
            "synonyms",
            "substances",
            "public_comments",
            "status",
        )
        read_only_fields = fields
