from rest_framework import serializers

from data.models import Declarant, Supervisor


class BaseRoleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "name")

    def get_name(self, obj):
        return obj.__class__.__name__


# Pour l'instant, pas besoin de CompanyRoleSerializer car on ne veut pas injecter la donnée
# class CompanyRoleSerializer(BaseRoleSerializer):
#     companies = CompanySerializer(many=True, read_only=True)

#     class Meta:
#         abstract = True
#         fields = BaseRoleSerializer.Meta.fields + ("companies",)


class SupervisorSerializer(BaseRoleSerializer):
    class Meta:
        model = Supervisor
        fields = BaseRoleSerializer.Meta.fields


class DeclarantSerializer(BaseRoleSerializer):
    class Meta:
        model = Declarant
        fields = BaseRoleSerializer.Meta.fields
