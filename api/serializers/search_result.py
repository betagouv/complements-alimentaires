from rest_framework import serializers
from data.models import Plant, Microorganism, Ingredient, Substance


class SearchResultSerializer(serializers.Serializer):
    object_type = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    def get_object_type(self, instance):
        if isinstance(instance, Plant):
            return "plant"
        if isinstance(instance, Microorganism):
            return "microorganism"
        if isinstance(instance, Ingredient):
            return "ingredient"
        if isinstance(instance, Substance):
            return "substance"
