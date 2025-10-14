from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from data.models import (
    Part,
    Plant,
    PlantFamily,
    PlantMaxQuantityPerPopulationRelation,
    PlantPart,
    PlantSynonym,
    Population,
)

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


class PlantFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantFamily
        fields = (
            "id",
            "name",
            "is_obsolete",
            "name_en",
            "siccrf_id",
        )
        read_only_fields = fields


class PlantPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ("id", "name")


class PartRelationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="plantpart.name")
    name_en = serializers.CharField(source="plantpart.name_en")
    is_obsolete = serializers.BooleanField(source="plantpart.is_obsolete")
    siccrf_id = serializers.IntegerField(source="plantpart.siccrf_id")
    id = serializers.IntegerField(source="plantpart.id")

    class Meta:
        model = Part
        fields = ("id", "name", "name_en", "is_obsolete", "siccrf_id", "must_be_monitored", "is_useful")
        read_only_fields = fields


class PlantSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSynonym
        fields = (
            "name",
            "standard_name",
            "synonym_type",
        )
        read_only_fields = fields


class PlantMaxQuantitySerializer(serializers.ModelSerializer):
    population = SimplePopulationSerializer()

    class Meta:
        model = PlantMaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")
        read_only_fields = fields


class PlantSerializer(CommonIngredientReadSerializer):
    family = PlantFamilySerializer(read_only=True)
    plant_parts = PartRelationSerializer(source="part_set", many=True, read_only=True)
    synonyms = PlantSynonymSerializer(many=True, read_only=True, source="plantsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    max_quantities = PlantMaxQuantitySerializer(
        many=True, source="plantmaxquantityperpopulationrelation_set", required=False
    )

    class Meta:
        model = Plant
        fields = COMMON_FETCH_FIELDS + (
            "family",
            "plant_parts",
            "substances",
        )
        read_only_fields = fields


class PlantSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSynonym
        fields = (
            "name",
            "synonym_type",
        )


class PlantPartModificationSerializer(serializers.ModelSerializer):
    plantpart = serializers.PrimaryKeyRelatedField(queryset=PlantPart.objects.all())
    is_useful = serializers.BooleanField()

    class Meta:
        model = Part
        fields = (
            "plantpart",
            "is_useful",
        )


class PlantMaxQuantityModificationSerializer(serializers.ModelSerializer):
    population = serializers.PrimaryKeyRelatedField(queryset=Population.objects.all())

    class Meta:
        model = PlantMaxQuantityPerPopulationRelation
        fields = ("max_quantity", "population")


class PlantModificationSerializer(CommonIngredientModificationSerializer, WithSubstances):
    synonyms = PlantSynonymModificationSerializer(many=True, source="plantsynonym_set", required=False)
    max_quantities = PlantMaxQuantityModificationSerializer(
        many=True, source="plantmaxquantityperpopulationrelation_set", required=False
    )
    plant_parts = PlantPartModificationSerializer(source="part_set", many=True)

    synonym_model = PlantSynonym
    synonym_set_field_name = "plantsynonym_set"
    max_quantities_model = PlantMaxQuantityPerPopulationRelation
    max_quantities_set_field_name = "plantmaxquantityperpopulationrelation_set"
    ingredient_name_field = "plant"
    declaredingredient_set_field_names = ["declaredplant_set"]

    class Meta:
        model = Plant
        fields = (
            COMMON_FIELDS
            + COMMON_NAME_FIELDS
            + (
                "family",
                "plant_parts",
                "substances",
            )
        )
        read_only = COMMON_READ_ONLY_FIELDS

    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    @transaction.atomic
    def create(self, validated_data):
        parts = validated_data.pop("part_set", [])
        plant = super().create(validated_data)

        PlantModificationSerializer._check_part_unicity(parts)

        for part in parts:
            Part.objects.create(plant=plant, plantpart=part["plantpart"], is_useful=part["is_useful"])

        return plant

    @transaction.atomic
    def update(self, instance, validated_data):
        parts = validated_data.pop("part_set", [])
        super().update(instance, validated_data)

        ids_to_keep_or_create = PlantModificationSerializer._check_part_unicity(parts)
        instance.part_set.exclude(plantpart__id__in=ids_to_keep_or_create).delete()

        for part in parts:
            existing_part = instance.part_set.filter(plantpart=part["plantpart"])
            if existing_part.exists():
                existing_part = existing_part.first()
                existing_part.is_useful = part["is_useful"]
                existing_part.save()
            else:
                Part.objects.create(plant=instance, plantpart=part["plantpart"], is_useful=part["is_useful"])

        return instance

    def _check_part_unicity(parts):
        ids_to_keep_or_create = [part["plantpart"].id for part in parts]

        if len(list(set(ids_to_keep_or_create))) < len(ids_to_keep_or_create):
            raise ParseError(detail="Chaque partie de plante devrait utilisée au maximum une fois")

        return ids_to_keep_or_create
