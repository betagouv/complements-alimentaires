from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import IngredientStatus, Microorganism, MicroorganismSynonym

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
    modification_date = serializers.DateTimeField(format="%Y-%m-%d", required=False)

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
            "modification_date",
        )
        read_only_fields = fields
