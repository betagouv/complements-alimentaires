from rest_framework import serializers

from data.models import Snapshot

from .user import SimpleUserSerializer


class SnapshotSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Snapshot

        fields = [
            "creation_date",
            "comment",
            "status",
            "json_declaration",
            "user",
            "id",
            "action",
            "post_validation_status",
            "effective_withdrawal_date",
        ]
        read_only_fields = fields
