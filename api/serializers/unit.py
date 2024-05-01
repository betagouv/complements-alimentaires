from rest_framework import serializers
from data.models import SubstanceUnit


class SubstanceUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstanceUnit
        fields = [
            "id",
            "name",
            "long_name",
        ]
        read_only_fields = fields
