from django.contrib.auth import get_user_model

from rest_framework import serializers

from data.models import CoSupervisionClaim
from data.models.company import CompanyRoleClassChoices


class CoSupervisionClaimSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name")

    class Meta:
        model = CoSupervisionClaim
        fields = ("id", "creation_date", "sender_name", "description")
        read_only_fields = fields


class AddNewCollaboratorSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    roles = serializers.ListField(child=serializers.ChoiceField(choices=CompanyRoleClassChoices))

    def validate_recipient_email(self, value):
        normalized_email = get_user_model().objects.normalize_email(value)
        return normalized_email
