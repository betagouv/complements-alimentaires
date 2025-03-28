from rest_framework import serializers

from data.models import ErrorReport


class ErrorReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = (
            "id",
            "email",
            "author",
            "status",
            "message",
            "plant",
            "ingredient",
            "microorganism",
            "substance",
        )
        read_only_fields = (
            "status",
            "author",
            "id",
        )
