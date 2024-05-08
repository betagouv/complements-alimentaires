from rest_framework import serializers

from data.models.solicitation import CoSupervisionClaim


class CoSupervisionClaimSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name")

    class Meta:
        model = CoSupervisionClaim
        fields = ("id", "creation_date", "sender_name", "description")
        read_only_fields = fields
