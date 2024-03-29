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


class CompanySupervisorSerializer(BaseRoleSerializer):
    companies = CompanySerializer(many=True, read_only=True)

    class Meta:
        model = CompanySupervisor
        fields = BaseRoleSerializer.Meta.fields + ("companies",)


class DeclarantSerializer(BaseRoleSerializer):
    class Meta:
        model = Declarant
        fields = BaseRoleSerializer.Meta.fields + ()
