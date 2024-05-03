from rest_framework import serializers

from data.models.solicitation import Solicitation


class UnprocessedSolicitationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name")

    class Meta:
        model = Solicitation
        fields = ("id", "creation_date", "kind", "sender_name", "description")
        read_only_fields = fields
