from rest_framework import serializers
from data.models import Microorganism, MicroorganismSynonym


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

    class Meta:
        model = Microorganism
        fields = (
            "id",
            "name",
            "name_en",
            "genre",
            "synonyms",
        )
        read_only_fields = fields
