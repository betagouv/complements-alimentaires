from rest_framework import serializers
from django.contrib.auth import get_user_model
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


class LoggedUserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "roles")
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


class UserInputSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # prevent to return hash in response

    class Meta:
        model = User
        fields = ("username", "email", "last_name", "first_name", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
