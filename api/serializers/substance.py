from rest_framework import serializers
from data.models import Substance, SubstanceSynonym


class SubstanceSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class SubstanceSerializer(serializers.ModelSerializer):
    synonyms = SubstanceSynonymSerializer(many=True, read_only=True, source="substancesynonym_set")
    unit = serializers.CharField(read_only=True, source="unit.name")
    status = serializers.CharField(read_only=True, source="status.name")

    class Meta:
        model = Substance
        fields = (
            "id",
            "name",
            "name_en",
            "cas_number",
            "einec_number",
            "source",
            "must_specify_quantity",
            "max_quantity",
            "nutritional_reference",
            "unit",
            "synonyms",
            "public_comments",
            "status",
        )
        read_only_fields = fields


class SubstanceShortSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(read_only=True, source="unit.name")

    class Meta:
        model = Substance
        fields = (
            "id",
            "name",
            "name_en",
            "cas_number",
            "einec_number",
            "unit",
        )
        read_only_fields = fields
