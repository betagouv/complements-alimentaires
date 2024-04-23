from rest_framework import serializers
from data.models import Substance, SubstanceSynonym, IngredientStatus
from api.utils.choice_field import GoodReprChoiceField


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
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)

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
