from django.db import transaction

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
    substances = serializers.PrimaryKeyRelatedField(many=True, queryset=Substance.objects.all(), required=False)


class WithName(serializers.ModelSerializer):
    name = serializers.CharField(source="ca_name")


class CommonIngredientModificationSerializer(serializers.ModelSerializer):
    public_comments = serializers.CharField(source="ca_public_comments", required=False)
    private_comments = serializers.CharField(source="ca_private_comments", required=False)
    status = serializers.IntegerField(source="ca_status", required=False)

    # DRF ne gère pas automatiquement la création des nested-fields :
    # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    @transaction.atomic
    def create(self, validated_data):
        synonyms = validated_data.pop(self.synonym_set_field_name, [])
        ingredient = super().create(validated_data)

        for synonym in synonyms:
            self.add_synonym(ingredient, synonym)

        return ingredient

    @transaction.atomic
    def update(self, instance, validated_data):
        synonyms = validated_data.pop(self.synonym_set_field_name, [])
        super().update(instance, validated_data)

        try:
            new_synonym_list = [s["name"] for s in synonyms]
        except KeyError:
            raise ParseError(detail="Must provide 'name' to create new synonym")
        existing_synonyms = getattr(instance, self.synonym_set_field_name)

        # TODO: is it important to update, rather delete and recreate, 'new' synonyms ?
        synonyms_to_delete = existing_synonyms.exclude(name__in=new_synonym_list)
        synonyms_to_delete.delete()

        for synonym in synonyms:
            if not existing_synonyms.filter(name=synonym["name"]).exists():
                self.add_synonym(instance, synonym)

        return instance

    def add_synonym(self, instance, synonym):
        try:
            name = synonym["name"]
            if name and name != instance.name and not self.synonym_model.objects.filter(name=name).exists():
                self.synonym_model.objects.create(standard_name=instance, name=name)
        except KeyError:
            raise ParseError(detail="Must provide 'name' to create new synonym")
