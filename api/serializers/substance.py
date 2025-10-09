from rest_framework import serializers

from data.models import Population, Substance, SubstanceMaxQuantityPerPopulationRelation, SubstanceSynonym

from .common_ingredient import (
    COMMON_FETCH_FIELDS,
    COMMON_FIELDS,
    COMMON_NAME_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
)
from .population import SimplePopulationSerializer
from .utils import PrivateFieldsSerializer


class SubstanceSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = (
            "id",
            "name",
            "synonym_type",
        )
        read_only_fields = fields


class SubstanceMaxQuantitySerializer(serializers.ModelSerializer):
    population = SimplePopulationSerializer()

    class Meta:
        model = SubstanceMaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")
        read_only_fields = fields


class SubstanceSerializer(CommonIngredientReadSerializer):
    synonyms = SubstanceSynonymSerializer(many=True, read_only=True, source="substancesynonym_set")
    max_quantities = SubstanceMaxQuantitySerializer(
        many=True, source="substancemaxquantityperpopulationrelation_set", required=False
    )

    class Meta:
        model = Substance
        fields = COMMON_FETCH_FIELDS + (
            "cas_number",
            "einec_number",
            "must_specify_quantity",
            "max_quantity",
            "nutritional_reference",
            "substance_types",
        )
        read_only_fields = fields


class SubstanceShortSerializer(PrivateFieldsSerializer):
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")
    max_quantities = SubstanceMaxQuantitySerializer(
        many=True, source="substancemaxquantityperpopulationrelation_set", required=False
    )

    class Meta:
        model = Substance
        fields = (
            "id",
            "name",
            "cas_number",
            "einec_number",
            "unit",
            "unit_id",
            "max_quantities",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "must_specify_quantity",
        )
        read_only_fields = fields


class SubstanceSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = (
            "name",
            "synonym_type",
        )


class SubstanceMaxQuantityModificationSerializer(serializers.ModelSerializer):
    population = serializers.PrimaryKeyRelatedField(queryset=Population.objects.all())

    class Meta:
        model = SubstanceMaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")


class SubstanceModificationSerializer(CommonIngredientModificationSerializer):
    synonyms = SubstanceSynonymModificationSerializer(many=True, source="substancesynonym_set", required=False)
    max_quantities = SubstanceMaxQuantityModificationSerializer(
        many=True, source="substancemaxquantityperpopulationrelation_set", required=False
    )

    synonym_model = SubstanceSynonym
    synonym_set_field_name = "substancesynonym_set"
    max_quantities_model = SubstanceMaxQuantityPerPopulationRelation
    max_quantities_set_field_name = "substancemaxquantityperpopulationrelation_set"
    ingredient_name_field = "substance"
    declaredingredient_set_field_names = ["declaredsubstance_set", "computedsubstance_set"]

    class Meta:
        model = Substance
        fields = (
            COMMON_FIELDS
            + COMMON_NAME_FIELDS
            + (
                "cas_number",
                "einec_number",
                "max_quantity",  # une property du Model, set grâce à create() et update()
                "nutritional_reference",
                "must_specify_quantity",
                "substance_types",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS
