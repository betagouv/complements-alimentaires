from rest_framework import serializers

from data.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "id",
            "name",
            "long_name",
        ]
        read_only_fields = fields
