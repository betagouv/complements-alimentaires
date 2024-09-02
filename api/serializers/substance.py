from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import IngredientStatus, Substance, SubstanceSynonym

from .historical_record import HistoricalRecordField
from .utils import PrivateCommentSerializer


class SubstanceSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class SubstanceSerializer(PrivateCommentSerializer):
    synonyms = SubstanceSynonymSerializer(many=True, read_only=True, source="substancesynonym_set")
    unit = serializers.CharField(read_only=True, source="unit.name")
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
            "synonyms",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "activity",
            "status",
            "history",
            "object_type",
        )
        read_only_fields = fields


class SubstanceShortSerializer(PrivateCommentSerializer):
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
            "max_quantity",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
        )
        read_only_fields = fields
