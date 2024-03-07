from rest_framework import serializers


class AutocompleteItemSerializer(serializers.Serializer):
    # Common
    autocomplete_match = serializers.CharField(read_only=True)
    object_type = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    # Ingredient
    description = serializers.CharField(read_only=True)

    # Substance
    cas_number = serializers.CharField(read_only=True)
    einec_number = serializers.CharField(read_only=True)

    # Microorganism
    genre = serializers.CharField(read_only=True)
