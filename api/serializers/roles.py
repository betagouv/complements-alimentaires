from rest_framework import serializers

from data.models import CompanySupervisor, Declarant


class BaseRoleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "name", "display_name")

    def get_name(self, obj):
        return obj.__class__.__name__

    def get_display_name(self, obj):
        return obj._meta.verbose_name.capitalize()


# Pour l'instant, pas besoin de CompanyRoleSerializer car on ne veut pas injecter la donnée
# class CompanyRoleSerializer(BaseRoleSerializer):
#     companies = CompanySerializer(many=True, read_only=True)

#     class Meta:
#         abstract = True
#         fields = BaseRoleSerializer.Meta.fields + ("companies",)


class CompanySupervisorSerializer(BaseRoleSerializer):
    class Meta:
        model = CompanySupervisor
        fields = BaseRoleSerializer.Meta.fields


class DeclarantSerializer(BaseRoleSerializer):
    class Meta:
        model = Declarant
        fields = BaseRoleSerializer.Meta.fields
