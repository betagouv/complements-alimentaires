from rest_framework import serializers

from data.models import ControlRole, InstructionRole, VisaRole


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


class VisaRoleSerializer(BaseGlobalRoleSerializer):
    class Meta:
        model = VisaRole
        fields = BaseGlobalRoleSerializer.Meta.fields


class ControlRoleSerializer(BaseGlobalRoleSerializer):
    class Meta:
        model = ControlRole
        fields = BaseGlobalRoleSerializer.Meta.fields


class SimpleInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionRole
        fields = ("id", "name")
        read_only_fields = fields


class SimpleVisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaRole
        fields = ("id", "name")
        read_only_fields = fields


class SimpleControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlRole
        fields = ("id", "name")
        read_only_fields = fields
