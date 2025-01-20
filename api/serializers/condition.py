from rest_framework import serializers

from data.models import Condition


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = [
            "name",
            "id",
            "name_en",
            "min_age",
            "max_age",
            "category",
        ]
        read_only_fields = fields
