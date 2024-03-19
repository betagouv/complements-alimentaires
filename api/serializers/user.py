from rest_framework import serializers
from django.contrib.auth import get_user_model
from .roles import CompanySupervisorSerializer, DeclarantSerializer
from data.models import CompanySupervisor, Declarant


class BlogPostAuthor(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
        )


class LoggedUserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
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
