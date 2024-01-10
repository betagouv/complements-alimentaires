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
            "min_quantity",
            "max_quantity",
            "nutritional_reference",
            "synonyms",
            "public_comments",
        )
        read_only_fields = fields


class SubstanceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substance
        fields = (
            "id",
            "name",
            "name_en",
            "cas_number",
            "einec_number",
        )
        read_only_fields = fields
