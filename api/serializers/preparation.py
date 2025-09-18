from rest_framework import serializers

from data.models import Preparation


class PreparationSerializer(serializers.ModelSerializer):
    # TODO make a unique abstract class for all simple models (Condition, Effect, Preparation, Population...)
    class Meta:
        model = Preparation
        fields = [
            "id",
            "name",
            "name_en",
        ]
        read_only_fields = fields
