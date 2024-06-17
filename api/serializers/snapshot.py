from rest_framework import serializers

from data.models import Snapshot

from .user import SimpleUserSerializer


class SnapshotSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Snapshot

        fields = ["creation_date", "comment", "status", "json_declaration", "user", "id"]
        read_only_fields = fields
