from rest_framework import serializers
from data.models import Plant, Microorganism, Ingredient, Substance


class SearchResultSerializer(serializers.Serializer):
    # Common
    object_type = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    name_en = serializers.CharField(read_only=True)

    # Ingredient
    description = serializers.CharField(read_only=True)
    observation = serializers.CharField(read_only=True)

    # Substance
    cas_number = serializers.CharField(read_only=True)
    einec_number = serializers.CharField(read_only=True)
    source = serializers.CharField(read_only=True)

    # Microorganism
    genre = serializers.CharField(read_only=True)

    def get_object_type(self, instance):
        if isinstance(instance, Plant):
            return "plant"
        if isinstance(instance, Microorganism):
            return "microorganism"
        if isinstance(instance, Ingredient):
            return "ingredient"
        if isinstance(instance, Substance):
            return "substance"
