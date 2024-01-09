from rest_framework import serializers
from data.models import Plant, PlantFamily, PlantPart, PlantSynonym
from .substance import SubstanceShortSerializer


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
        fields = (
            "name",
            "is_obsolete",
            "name_en",
            "siccrf_id",
        )
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


class PlantSerializer(serializers.ModelSerializer):
    family = PlantFamilySerializer(read_only=True)
    useful_parts = PlantPartSerializer(many=True, read_only=True)
    synonyms = PlantSynonymSerializer(many=True, read_only=True, source="plantsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = (
            "id",
            "name",
            "family",
            "useful_parts",
            "synonyms",
            "substances",
        )
        read_only_fields = fields
