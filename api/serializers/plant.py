from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import IngredientStatus, Part, Plant, PlantFamily, PlantPart, PlantSynonym

from .historical_record import HistoricalRecordField
from .substance import SubstanceShortSerializer
from .utils import PrivateCommentSerializer


class PlantFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantFamily
        fields = (
            "name",
            "is_obsolete",
            "name_en",
            "siccrf_id",
        )
        read_only_fields = fields


class PlantPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ("id", "name")


class PartRelationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="plantpart.name")
    name_en = serializers.CharField(source="plantpart.name_en")
    is_obsolete = serializers.BooleanField(source="plantpart.is_obsolete")
    siccrf_id = serializers.IntegerField(source="plantpart.siccrf_id")
    id = serializers.IntegerField(source="plantpart.id")

    class Meta:
        model = Part
        fields = ("id", "name", "name_en", "is_obsolete", "siccrf_id", "must_be_monitored", "is_useful")
        read_only_fields = fields


class PlantSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSynonym
        fields = (
            "name",
            "is_obsolete",
            "standard_name",
        )
        read_only_fields = fields


class PlantSerializer(PrivateCommentSerializer):
    family = PlantFamilySerializer(read_only=True)
    plant_parts = PartRelationSerializer(source="part_set", many=True, read_only=True)
    synonyms = PlantSynonymSerializer(many=True, read_only=True, source="plantsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Plant
        fields = (
            "id",
            "name",
            "family",
            "plant_parts",
            "synonyms",
            "substances",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "activity",
            "status",
            "history",
        )
        read_only_fields = fields
