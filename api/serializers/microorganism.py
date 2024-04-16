from rest_framework import serializers
from data.models import Microorganism, MicroorganismSynonym
from .substance import SubstanceShortSerializer


class MicroorganismSynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroorganismSynonym
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


class MicroorganismSerializer(serializers.ModelSerializer):
    synonyms = MicroorganismSynonymSerializer(many=True, read_only=True, source="microorganismsynonym_set")
    substances = SubstanceShortSerializer(many=True, read_only=True)
    status = serializers.CharField(read_only=True, source="status.name")

    class Meta:
        model = Microorganism
        fields = (
            "id",
            "name",
            "genus",
            "species",
            "synonyms",
            "substances",
            "public_comments",
            "status",
        )
        read_only_fields = fields
