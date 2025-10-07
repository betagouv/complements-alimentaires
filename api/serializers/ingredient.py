from rest_framework import serializers

from data.models import Ingredient, IngredientMaxQuantityPerPopulationRelation, IngredientSynonym, Population

from .common_ingredient import (
    COMMON_FETCH_FIELDS,
    COMMON_FIELDS,
    COMMON_NAME_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
    WithSubstances,
)
from .population import SimplePopulationSerializer
from .substance import SubstanceShortSerializer


class IngredientSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientSynonym
        fields = (
            "id",
            "name",
            "synonym_type",
        )
        read_only_fields = fields


class IngredientMaxQuantitySerializer(serializers.ModelSerializer):
    population = SimplePopulationSerializer()

    class Meta:
        model = IngredientMaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")
        read_only_fields = fields


class IngredientSerializer(CommonIngredientReadSerializer):
    synonyms = IngredientSynonymSerializer(many=True, read_only=True, source="ingredientsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")

    max_quantities = IngredientMaxQuantitySerializer(
        many=True, source="ingredientmaxquantityperpopulationrelation_set", required=False
    )

    class Meta:
        model = Ingredient
        fields = COMMON_FETCH_FIELDS + ("substances",)
        read_only_fields = fields


class IngredientSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientSynonym
        fields = (
            "name",
            "synonym_type",
        )


class IngredientMaxQuantityModificationSerializer(serializers.ModelSerializer):
    population = serializers.PrimaryKeyRelatedField(queryset=Population.objects.all())

    class Meta:
        model = IngredientMaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")


class IngredientModificationSerializer(CommonIngredientModificationSerializer, WithSubstances):
    synonyms = IngredientSynonymModificationSerializer(many=True, source="ingredientsynonym_set", required=False)
    max_quantities = IngredientMaxQuantityModificationSerializer(
        many=True, source="ingredientmaxquantityperpopulationrelation_set", required=False
    )

    synonym_model = IngredientSynonym
    synonym_set_field_name = "ingredientsynonym_set"
    max_quantities_model = IngredientMaxQuantityPerPopulationRelation
    max_quantities_set_field_name = "ingredientmaxquantityperpopulationrelation_set"
    ingredient_name_field = "ingredient"

    declaredingredient_set_field_names = ["declaredingredient_set"]

    class Meta:
        model = Ingredient
        fields = (
            COMMON_FIELDS
            + COMMON_NAME_FIELDS
            + (
                "ingredient_type",
                "substances",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS
