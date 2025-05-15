from rest_framework import serializers

from data.models import Microorganism, MicroorganismSynonym

from .substance import SubstanceShortSerializer
from .common_ingredient import (
    COMMON_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    COMMON_FETCH_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
    WithSubstances,
)


class MicroorganismSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroorganismSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class MicroorganismSerializer(CommonIngredientReadSerializer):
    synonyms = MicroorganismSynonymSerializer(many=True, read_only=True, source="microorganismsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)

    class Meta:
        model = Microorganism
        fields = COMMON_FETCH_FIELDS + (
            "genus",
            "species",
            "substances",
        )
        read_only_fields = fields


class MicroorganismSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroorganismSynonym
        fields = ("name",)


class MicroorganismModificationSerializer(CommonIngredientModificationSerializer, WithSubstances):
    synonyms = MicroorganismSynonymModificationSerializer(many=True, source="microorganismsynonym_set", required=False)
    genus = serializers.CharField(source="ca_genus")
    species = serializers.CharField(source="ca_species")

    synonym_model = MicroorganismSynonym
    synonym_set_field_name = "microorganismsynonym_set"

    declaredingredient_set_field_names = ["declaredmicroorganism_set"]

    class Meta:
        model = Microorganism
        fields = COMMON_FIELDS + (
            "genus",
            "species",
            "substances",
        )
        read_only = COMMON_READ_ONLY_FIELDS
