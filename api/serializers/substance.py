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


class SubstanceSerializer(CommonIngredientReadSerializer):
    synonyms = SubstanceSynonymSerializer(many=True, read_only=True, source="substancesynonym_set")
    unit = serializers.CharField(read_only=True, source="unit.name")
    unit_id = serializers.IntegerField(read_only=True, source="unit.id")

    class Meta:
        model = Substance
        fields = COMMON_FETCH_FIELDS + (
            "name_en",
            "cas_number",
            "einec_number",
            "source",
            "must_specify_quantity",
            "max_quantity",
            "nutritional_reference",
            "unit",
            "unit_id",
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
                "max_quantities",
                "nutritional_reference",
                "unit",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS

    @transaction.atomic
    def create(self, validated_data):
        max_quantities = validated_data.pop("maxquantityperpopulationrelation_set", None)
        substance = super().create(validated_data)
        if max_quantities is not None:
            for max_quantity in max_quantities:
                # TODO: what if bad name is passed?
                population = Population.objects.get(name=max_quantity["population"]["name"])
                MaxQuantityPerPopulationRelation.objects.create(
                    substance=substance, population=population, ca_max_quantity=max_quantity["ca_max_quantity"]
                )

        return substance

    @transaction.atomic
    def update(self, instance, validated_data):
        max_quantities = validated_data.pop("maxquantityperpopulationrelation_set", None)
        substance = super().update(instance, validated_data)

        if max_quantities is not None:
            # TODO: delete missing lines
            # synonyms_to_delete = existing_synonyms.exclude(name__in=new_synonym_list)
            # synonyms_to_delete.delete()

            for max_quantity in max_quantities:
                print(max_quantity)
                population_name = max_quantity["population"]["name"]
                population = Population.objects.get(name=population_name)
                max_quantity_value = max_quantity["ca_max_quantity"]

                # TODO: what happens if bad population name is given
                # TODO: what happens if population or max quantity is missing
                # TODO: block add/update if substance doesn't have a unit set

                existing_relation = MaxQuantityPerPopulationRelation.objects.filter(
                    substance=substance, population=population
                )
                print(existing_relation.exists())
                if existing_relation.exists():
                    existing_relation = existing_relation.first()
                    if existing_relation.max_quantity != max_quantity_value:
                        existing_relation.ca_max_quantity = max_quantity_value
                        existing_relation.save()
                else:
                    MaxQuantityPerPopulationRelation.objects.create(
                        substance=substance, population=population, ca_max_quantity=max_quantity_value
                    )

            # general_population = Population.objects.get(name="Population générale")
            # max_qty_general_pop = MaxQuantityPerPopulationRelation.objects.filter(
            #     substance=substance, population=general_population
            # )

            # # delete
            # if max_qty_general_pop.exists() and max_quantity is None:
            #     max_qty_general_pop.first().delete()
            # # update
            # elif max_qty_general_pop.exists() and max_quantity is not None:
            #     max_quantity_to_change = max_qty_general_pop.first()
            #     max_quantity_to_change.ca_max_quantity = max_quantity
            #     max_quantity_to_change.save()
            # # create
            # elif not max_qty_general_pop.exists() and max_quantity is not None:
            #     MaxQuantityPerPopulationRelation.objects.create(
            #         substance=substance, population=general_population, ca_max_quantity=max_quantity
            #     )

        return substance
