from rest_framework import serializers
from data.models import CompanySupervisor, Declarant
from .company import CompanySerializer


class BaseRoleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        abstract = True
        fields = ("id", "name", "display_name")

    def get_name(self, obj):
        return obj.__class__.__name__

    def get_display_name(self, obj):
        return obj._meta.verbose_name.capitalize()


class CompanyRoleSerializer(BaseRoleSerializer):
    companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        abstract = True
        fields = BaseRoleSerializer.Meta.fields + ("companies",)


class CompanySupervisorSerializer(CompanyRoleSerializer):
    class Meta:
        model = CompanySupervisor
        fields = CompanyRoleSerializer.Meta.fields


class DeclarantSerializer(CompanyRoleSerializer):
    class Meta:
        model = Declarant
        fields = CompanyRoleSerializer.Meta.fields
