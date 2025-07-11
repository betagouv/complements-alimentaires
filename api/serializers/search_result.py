from rest_framework import serializers

from api.utils.choice_field import GoodReprChoiceField
from data.models import Ingredient, IngredientStatus, Microorganism, Plant, Substance


class SearchResultSerializer(serializers.Serializer):
    # Common
    object_type = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    name_en = serializers.CharField(read_only=True)
    status = GoodReprChoiceField(choices=IngredientStatus.choices, read_only=True)
    is_novel_food = serializers.BooleanField(read_only=True)

    # Ingredient
    description = serializers.CharField(read_only=True)

    # Substance
    cas_number = serializers.CharField(read_only=True)
    einec_number = serializers.CharField(read_only=True)
    source = serializers.CharField(read_only=True)

    # Microorganism
    genre = serializers.CharField(read_only=True)
    match = serializers.CharField(read_only=True, source="autocomplete_match")

    def get_synonyms(self, instance):
        if isinstance(instance, Plant):
            return instance.plantsynonym_set.values_list("name", flat=True).distinct()
        if isinstance(instance, Microorganism):
            return instance.microorganismsynonym_set.values_list("name", flat=True).distinct()
        if isinstance(instance, Ingredient):
            return instance.ingredientsynonym_set.values_list("name", flat=True).distinct()
        if isinstance(instance, Substance):
            return instance.substancesynonym_set.values_list("name", flat=True).distinct()
