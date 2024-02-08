from rest_framework import serializers
from data.models import Condition


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = [
            "name",
            "id",
            "name_en",
        ]
        read_only_fields = fields
