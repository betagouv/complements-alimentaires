from rest_framework import serializers
from rest_framework.exceptions import ParseError

from api.utils.choice_field import GoodReprChoiceField
from data.models import IngredientStatus, Part, Plant, PlantFamily, PlantPart, PlantSynonym, Substance

from .historical_record import HistoricalRecordField
from .substance import SubstanceShortSerializer
from .utils import HistoricalModelSerializer, PrivateFieldsSerializer


class PlantFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantFamily
        fields = (
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
            "is_obsolete",
            "standard_name",
        )
        read_only_fields = fields


class PlantSerializer(HistoricalModelSerializer, PrivateFieldsSerializer):
    family = PlantFamilySerializer(read_only=True)
    plant_parts = PartRelationSerializer(source="part_set", many=True, read_only=True)
    synonyms = PlantSynonymSerializer(many=True, read_only=True, source="plantsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Plant
        fields = (
            "id",
            "name",
            "family",
            "plant_parts",
            "synonyms",
            "substances",
            "public_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "activity",
            "status",
            "novel_food",
            "history",
        )
        read_only_fields = fields


class PlantSynonymModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSynonym
        fields = ("name",)


class PlantModificationSerializer(serializers.ModelSerializer):
    synonyms = PlantSynonymModificationSerializer(many=True, source="plantsynonym_set")
    plant_parts = serializers.PrimaryKeyRelatedField(many=True, queryset=PlantPart.objects.all())
    substances = serializers.PrimaryKeyRelatedField(many=True, queryset=Substance.objects.all())

    class Meta:
        model = Plant
        fields = (
            "id",
            "ca_name",
            "name",
            "ca_family",
            "plant_parts",
            "synonyms",
            "substances",  # TODO: should I be setting ca_is_related?
            "ca_public_comments",
            "public_comments",
            "ca_private_comments",
            "private_comments",  # Caché si l'utilisateur.ice ne fait pas partie de l'administration
            "activity",
            "ca_status",
            "novel_food",
            # "history",
        )
        read_only = (
            "id",
            "name",
            "public_comments",
            "private_comments",
            "activity",
        )

    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    def create(self, validated_data):
        synonyms = validated_data.pop("plantsynonym_set", [])
        plant = super().create(validated_data)

        synonym_model = PlantSynonym
        for synonym in synonyms:
            try:
                name = synonym["name"]
                if name and name != plant.name and not synonym_model.objects.filter(name=name).exists():
                    synonym_model.objects.create(standard_name=plant, name=name)
            except KeyError:
                raise ParseError(detail="Must provide 'name' to create new synonym")

        return plant
