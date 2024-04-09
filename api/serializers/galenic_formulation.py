from rest_framework import serializers
from data.models import GalenicFormulation


class GalenicFormulationSerializer(serializers.ModelSerializer):
    # TODO make a unique abstract class for all simple models (Condition, Effect, GalenicFormulation, Population...)
    class Meta:
        model = GalenicFormulation
        fields = [
            "name",
            "id",
            "name_en",
        ]
        read_only_fields = fields
