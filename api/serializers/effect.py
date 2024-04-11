from rest_framework import serializers
from data.models import Effect


class EffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = [
            "name",
            "id",
            "name_en",
        ]
        read_only_fields = fields
