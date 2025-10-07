from rest_framework import serializers

from data.models import Microorganism, MicroorganismMaxQuantityPerPopulationRelation, MicroorganismSynonym

from .common_ingredient import (
    COMMON_FETCH_FIELDS,
    COMMON_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
    WithSubstances,
)
from .population import SimplePopulationSerializer
from .substance import SubstanceShortSerializer


class MicroorganismSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroorganismSynonym
        fields = (
            "id",
            "name",
            "synonym_type",
        )
        read_only_fields = fields


class MicroorganismMaxQuantitySerializer(serializers.ModelSerializer):
    population = SimplePopulationSerializer()

    class Meta:
        model = MicroorganismMaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")
        read_only_fields = fields


class MicroorganismSerializer(CommonIngredientReadSerializer):
    synonyms = MicroorganismSynonymSerializer(many=True, read_only=True, source="microorganismsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")

    max_quantities = MicroorganismMaxQuantitySerializer(
        many=True, source="microorganismmaxquantityperpopulationrelation_set", required=False
    )

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
        fields = (
            "name",
            "synonym_type",
        )


class MicroorganismModificationSerializer(CommonIngredientModificationSerializer, WithSubstances):
    synonyms = MicroorganismSynonymModificationSerializer(many=True, source="microorganismsynonym_set", required=False)

    synonym_model = MicroorganismSynonym
    synonym_set_field_name = "microorganismsynonym_set"
    max_quantities_model = MicroorganismMaxQuantityPerPopulationRelation
    max_quantities_set_field_name = "microorganismmaxquantityperpopulationrelation_set"
    ingredient_name_field = "microorganism"
    max_quantities = MicroorganismMaxQuantitySerializer(
        many=True, source="microorganismmaxquantityperpopulationrelation_set", required=False
    )
    declaredingredient_set_field_names = ["declaredmicroorganism_set"]

    class Meta:
        model = Microorganism
        fields = COMMON_FIELDS + (
            "genus",
            "species",
            "substances",
        )
        read_only = COMMON_READ_ONLY_FIELDS
