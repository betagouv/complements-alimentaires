from rest_framework import serializers
from django.contrib.auth import get_user_model


class BlogPostAuthor(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
        )


class LoggedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = fields
