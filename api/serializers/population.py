from rest_framework import serializers

from data.models import Population


class PopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = [
            "name",
            "id",
            "is_obsolete",
            "min_age",
            "max_age",
            "category",
        ]
        read_only_fields = fields


class SimplePopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Population
        fields = ("id", "name")
        read_only_fields = fields
