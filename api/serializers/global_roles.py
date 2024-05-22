from rest_framework import serializers

from data.models import InstructionRole


class BaseGlobalRoleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "name")

    def get_name(self, obj):
        return obj.__class__.__name__


class InstructionRoleSerializer(BaseGlobalRoleSerializer):
    class Meta:
        model = InstructionRole
        fields = BaseGlobalRoleSerializer.Meta.fields
