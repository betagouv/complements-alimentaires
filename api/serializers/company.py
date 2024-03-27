from rest_framework import serializers
from data.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "social_name", "commercial_name", "siret")
