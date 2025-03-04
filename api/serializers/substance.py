from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import IngredientStatus, Population
from data.models.substance import MaxQuantityPerPopulationRelation, Substance, SubstanceSynonym

from .common_ingredient import (
    COMMON_FIELDS,
    COMMON_NAME_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    CommonIngredientModificationSerializer,
    WithName,
)
from .historical_record import HistoricalRecordField
from .utils import HistoricalModelSerializer, PrivateFieldsSerializer


class SubstanceSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class SubstanceSerializer(HistoricalModelSerializer, PrivateFieldsSerializer):
    synonyms = SubstanceSynonymSerializer(many=True, read_only=True, source="substancesynonym_set")
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    history = HistoricalRecordField(read_only=True)

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
            "unit_id",
            "synonyms",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "activity",
            "status",
            "novel_food",
            "history",
            "object_type",
        )
        read_only_fields = fields


class SubstanceShortSerializer(PrivateFieldsSerializer):
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")

    class Meta:
        model = Substance
        fields = (
            "id",
            "name",
            "name_en",
            "cas_number",
            "einec_number",
            "unit",
            "unit_id",
            "max_quantity",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "must_specify_quantity",
        )
        read_only_fields = fields


class SubstanceSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = ("name",)


class SubstanceModificationSerializer(CommonIngredientModificationSerializer, WithName):
    synonyms = SubstanceSynonymModificationSerializer(many=True, source="substancesynonym_set", required=False)
    cas_number = serializers.CharField(source="ca_cas_number", required=False, allow_blank=True)
    einec_number = serializers.CharField(source="ca_einec_number", required=False, allow_blank=True)
    max_quantity = serializers.FloatField(source="ca_max_quantity", required=False, allow_null=True)
    nutritional_reference = serializers.FloatField(source="ca_nutritional_reference", required=False, allow_null=True)

    synonym_model = SubstanceSynonym
    synonym_set_field_name = "substancesynonym_set"

    class Meta:
        model = Substance
        fields = (
            COMMON_FIELDS
            + COMMON_NAME_FIELDS
            + (
                "cas_number",
                "einec_number",
                "max_quantity",
                "nutritional_reference",
                "unit",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS
