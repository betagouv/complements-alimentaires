from rest_framework import serializers
from data.models import CompanySupervisor, Declarant
from .company import CompanySerializer


class BaseRoleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        abstract = True
        fields = (
            "id",
            "name",
        )

    def get_name(self, obj):
        return obj.__class__.__name__


class CompanySupervisorSerializer(BaseRoleSerializer):
    companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = CompanySupervisor
        fields = BaseRoleSerializer.Meta.fields + ("companies",)


class DeclarantSerializer(BaseRoleSerializer):
    class Meta:
        model = Declarant
        fields = BaseRoleSerializer.Meta.fields + ()
