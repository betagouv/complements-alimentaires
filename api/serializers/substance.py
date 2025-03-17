from django.db import transaction

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


class SubstanceMaxQuantityModificationSerializer(serializers.ModelSerializer):
    population = serializers.CharField(source="population.name")

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
                "max_quantity",  # une property du Model, set grâce à create() et update()
                "max_quantities",
                "nutritional_reference",
                "unit",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS

    @transaction.atomic
    def create(self, validated_data):
        # max_quantity doesn't exist in validated_data
        max_quantity = self.initial_data.get("max_quantity")
        substance = super().create(validated_data)
        general_population = Population.objects.get(name="Population générale")
        MaxQuantityPerPopulationRelation.objects.create(
            substance=substance, population=general_population, ca_max_quantity=max_quantity
        )

        return substance

    @transaction.atomic
    def update(self, instance, validated_data):
        max_quantity = self.initial_data.get("max_quantity")
        substance = super().update(instance, validated_data)

        general_population = Population.objects.get(name="Population générale")
        max_qty_general_pop = MaxQuantityPerPopulationRelation.objects.filter(
            substance=substance, population=general_population
        )

        if max_qty_general_pop.exists() and max_quantity:
            max_qty_general_pop.first().ca_max_quantity = max_quantity
            max_qty_general_pop.first().save()
        elif max_qty_general_pop.exists():
            max_qty_general_pop.first().delete()

        return substance
