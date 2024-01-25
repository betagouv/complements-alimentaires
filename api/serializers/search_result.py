from rest_framework import serializers
from data.models import Plant, Microorganism, Ingredient, Substance


class SearchResultSerializer(serializers.Serializer):
    # Common
    object_type = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    name_en = serializers.CharField(read_only=True)

    # Plant
    plantsynonym_set = serializers.SlugRelatedField(read_only=True, many=True, slug_field="name")

    # Ingredient
    description = serializers.CharField(read_only=True)
    observation = serializers.CharField(read_only=True)
    ingredientsynonym_set = serializers.SlugRelatedField(read_only=True, many=True, slug_field="name")

    # Substance
    cas_number = serializers.CharField(read_only=True)
    einec_number = serializers.CharField(read_only=True)
    source = serializers.CharField(read_only=True)
    substancesynonym_set = serializers.SlugRelatedField(read_only=True, many=True, slug_field="name")

    # Microorganism
    genre = serializers.CharField(read_only=True)
    microorganismsynonym = serializers.SlugRelatedField(read_only=True, many=True, slug_field="name")

    def get_object_type(self, instance):
        if isinstance(instance, Plant):
            return "plant"
        if isinstance(instance, Microorganism):
            return "microorganism"
        if isinstance(instance, Ingredient):
            return "ingredient"
        if isinstance(instance, Substance):
            return "substance"
