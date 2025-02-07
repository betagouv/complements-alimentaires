from rest_framework import serializers
from rest_framework.exceptions import ParseError

from data.models import Substance


COMMON_NAME_FIELDS = ("name",)

COMMON_FIELDS = (
    "id",
    "synonyms",
    "public_comments",
    "private_comments",
    "status",
    "novel_food",
)

COMMON_READ_ONLY_FIELDS = ("id",)


class WithSubstances(serializers.ModelSerializer):
    substances = serializers.PrimaryKeyRelatedField(many=True, queryset=Substance.objects.all())


class WithName(serializers.ModelSerializer):
    name = serializers.CharField(source="ca_name")


class CommonIngredientModificationSerializer(serializers.ModelSerializer):
    public_comments = serializers.CharField(source="ca_public_comments", required=False)
    private_comments = serializers.CharField(source="ca_private_comments", required=False)
    status = serializers.IntegerField(source="ca_status", required=False)

    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    def create(self, validated_data):
        synonyms = validated_data.pop(self.synonym_set_field_name, [])
        ingredient = super().create(validated_data)

        for synonym in synonyms:
            try:
                name = synonym["name"]
                if name and name != ingredient.name and not self.synonym_model.objects.filter(name=name).exists():
                    self.synonym_model.objects.create(standard_name=ingredient, name=name)
            except KeyError:
                raise ParseError(detail="Must provide 'name' to create new synonym")

        return ingredient
