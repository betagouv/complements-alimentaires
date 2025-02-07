from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import IngredientStatus, Microorganism, MicroorganismSynonym

from .historical_record import HistoricalRecordField
from .substance import SubstanceShortSerializer
from .utils import HistoricalModelSerializer, PrivateFieldsSerializer
from .common_ingredient import (
    COMMON_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    CommonIngredientModificationSerializer,
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


class MicroorganismSerializer(HistoricalModelSerializer, PrivateFieldsSerializer):
    synonyms = MicroorganismSynonymSerializer(many=True, read_only=True, source="microorganismsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    history = HistoricalRecordField(read_only=True)

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
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "activity",
            "status",
            "novel_food",
            "history",
        )
        read_only_fields = fields


class MicroorganismSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroorganismSynonym
        fields = ("name",)


class MicroorganismModificationSerializer(CommonIngredientModificationSerializer, WithSubstances):
    synonyms = MicroorganismSynonymModificationSerializer(many=True, source="microorganismsynonym_set")
    genus = serializers.CharField(source="ca_genus", required=False)
    species = serializers.CharField(source="ca_species", required=False)

    synonym_model = MicroorganismSynonym
    synonym_set_field_name = "microorganismsynonym_set"

    class Meta:
        model = Microorganism
        fields = COMMON_FIELDS + (
            "genus",
            "species",
            "substances",
        )
        read_only = COMMON_READ_ONLY_FIELDS
