from django.db import transaction

from rest_framework import serializers

from data.models import Population
from data.models.substance import MaxQuantityPerPopulationRelation, Substance, SubstanceSynonym

from .common_ingredient import (
    COMMON_FIELDS,
    COMMON_NAME_FIELDS,
    COMMON_READ_ONLY_FIELDS,
    COMMON_FETCH_FIELDS,
    CommonIngredientModificationSerializer,
    CommonIngredientReadSerializer,
    WithName,
)
from .utils import PrivateFieldsSerializer


class SubstanceSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ("id", "name")
        read_only_fields = fields


class SubstanceMaxQuantitySerializer(serializers.ModelSerializer):
    population = PopulationSerializer()

    class Meta:
        model = MaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")
        read_only_fields = fields


class SubstanceSerializer(CommonIngredientReadSerializer):
    synonyms = SubstanceSynonymSerializer(many=True, read_only=True, source="substancesynonym_set")
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")
    max_quantities = SubstanceMaxQuantitySerializer(
        many=True, source="maxquantityperpopulationrelation_set", required=False
    )

    class Meta:
        model = Substance
        fields = COMMON_FETCH_FIELDS + (
            "name_en",
            "cas_number",
            "einec_number",
            "source",
            "must_specify_quantity",
            "max_quantity",
            "max_quantities",
            "nutritional_reference",
            "unit",
            "unit_id",
        )
        read_only_fields = fields


class SubstanceShortSerializer(PrivateFieldsSerializer):
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")
    max_quantities = SubstanceMaxQuantitySerializer(
        many=True, source="maxquantityperpopulationrelation_set", required=False
    )

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
            "max_quantities",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "must_specify_quantity",
        )
        read_only_fields = fields


class SubstanceSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceSynonym
        fields = ("name",)


class SubstanceMaxQuantityModificationSerializer(serializers.ModelSerializer):
    population = serializers.PrimaryKeyRelatedField(queryset=Population.objects.all())
    max_quantity = serializers.FloatField(source="ca_max_quantity")

    class Meta:
        model = MaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")


class SubstanceModificationSerializer(CommonIngredientModificationSerializer, WithName):
    synonyms = SubstanceSynonymModificationSerializer(many=True, source="substancesynonym_set", required=False)
    cas_number = serializers.CharField(source="ca_cas_number", required=False, allow_blank=True)
    einec_number = serializers.CharField(source="ca_einec_number", required=False, allow_blank=True)
    max_quantities = SubstanceMaxQuantityModificationSerializer(
        many=True, source="maxquantityperpopulationrelation_set", required=False
    )
    must_specify_quantity = serializers.BooleanField(source="ca_must_specify_quantity", required=False)

    nutritional_reference = serializers.FloatField(source="ca_nutritional_reference", required=False, allow_null=True)

    synonym_model = SubstanceSynonym
    synonym_set_field_name = "substancesynonym_set"

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
                "max_quantities",
                "nutritional_reference",
                "unit",
                "must_specify_quantity",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS

    def validate_max_quantities(self, value):
        population_ids = [v["population"].id for v in value]
        unique_pop_ids = list(set(population_ids))
        if len(population_ids) != len(unique_pop_ids):
            raise serializers.ValidationError("Veuillez donner qu'une quantité maximale par population")
        return value

    @transaction.atomic
    def create(self, validated_data):
        max_quantities = validated_data.pop("maxquantityperpopulationrelation_set", None)
        substance = super().create(validated_data)
        if max_quantities is None:
            return substance

        for max_quantity in max_quantities:
            self.add_max_quantity(substance, max_quantity)

        return substance

    @transaction.atomic
    def update(self, instance, validated_data):
        max_quantities = validated_data.pop("maxquantityperpopulationrelation_set", None)
        substance = super().update(instance, validated_data)
        if max_quantities is None:
            return substance

        populations_to_keep = [q["population"] for q in max_quantities]
        substance.maxquantityperpopulationrelation_set.exclude(population__in=populations_to_keep).delete()

        for max_quantity in max_quantities:
            existing_q = substance.maxquantityperpopulationrelation_set.filter(
                population=max_quantity["population"].id
            )
            if existing_q.exists():
                existing_q = existing_q.first()
                existing_q.ca_max_quantity = max_quantity["ca_max_quantity"]
                existing_q.save()
            else:
                self.add_max_quantity(substance, max_quantity)

        return substance

    def add_max_quantity(self, substance, max_quantity):
        MaxQuantityPerPopulationRelation.objects.create(
            substance=substance, population=max_quantity["population"], ca_max_quantity=max_quantity["ca_max_quantity"]
        )
