from rest_framework import serializers

from data.models import Part, Plant, PlantFamily, PlantPart, PlantSynonym

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


class PlantFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantFamily
        fields = (
            "id",
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


class PlantSerializer(CommonIngredientReadSerializer):
    family = PlantFamilySerializer(read_only=True)
    plant_parts = PartRelationSerializer(source="part_set", many=True, read_only=True)
    synonyms = PlantSynonymSerializer(many=True, read_only=True, source="plantsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = COMMON_FETCH_FIELDS + (
            "family",
            "plant_parts",
            "substances",
        )
        read_only_fields = fields


class PlantSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSynonym
        fields = ("name",)


class PlantModificationSerializer(CommonIngredientModificationSerializer, WithSubstances, WithName):
    synonyms = PlantSynonymModificationSerializer(many=True, source="plantsynonym_set", required=False)
    plant_parts = serializers.PrimaryKeyRelatedField(many=True, queryset=PlantPart.objects.all())
    family = serializers.PrimaryKeyRelatedField(queryset=PlantFamily.objects.all(), source="ca_family")

    synonym_model = PlantSynonym
    synonym_set_field_name = "plantsynonym_set"

    class Meta:
        model = Plant
        fields = (
            COMMON_FIELDS
            + COMMON_NAME_FIELDS
            + (
                "family",
                "plant_parts",
                "substances",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS
