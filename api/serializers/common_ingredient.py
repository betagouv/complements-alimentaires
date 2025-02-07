from rest_framework import serializers
from rest_framework.exceptions import ParseError

from data.models import Substance


COMMON_NAME_FIELDS = (
    "ca_name",
    "name",
)

COMMON_FIELDS = (
    "id",
    "synonyms",
    "ca_public_comments",
    "public_comments",
    "ca_private_comments",
    "private_comments",
    "ca_status",
    "novel_food",
)

COMMON_READ_ONLY_FIELDS = (
    "id",
    "name",
    "public_comments",
    "private_comments",
)


class WithSubstances(serializers.ModelSerializer):
    substances = serializers.PrimaryKeyRelatedField(many=True, queryset=Substance.objects.all())


class CommonIngredientModificationSerializer(serializers.ModelSerializer):
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
