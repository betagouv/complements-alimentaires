from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from .roles import CompanySupervisorSerializer, DeclarantSerializer
from data.models import CompanySupervisor, Declarant

User = get_user_model()


class BlogPostAuthor(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "last_name", "first_name")


class LoggedUserSerializer(BaseUserSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + (
            "id",
            "roles",
        )
        read_only_fields = fields

    def get_roles(self, obj):
        roles_data = []

        # mapping of role models to their serializers
        role_serializer_mapping = {
            CompanySupervisor: CompanySupervisorSerializer,
            Declarant: DeclarantSerializer,
            # ... add new roles here
        }

        for model, serializer in role_serializer_mapping.items():
            # querying for role instances associated with the user
            role_instances = model.objects.filter(user=obj).active()

            # serializing role data
            for instance in role_instances:
                serializer_instance = serializer(instance)
                roles_data.append(serializer_instance.data)

        return roles_data


class CreateUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ("password",)

    password = serializers.CharField(
        write_only=True, required=True
    )  # empêche le retour du hash du mdp dans la réponse

    def validate_password(self, value):
        """Validate the password against settings-defined rules"""
        django_validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EditUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"confirm_new_password": "La confirmation ne correspond pas au mot de passe entré"}
            )
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError(
                {"confirm_new_password": "Le nouveau mot de passe est identique à l'actuel"}
            )
        django_validate_password(data["new_password"])
        return data
