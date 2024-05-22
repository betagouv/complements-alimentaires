from rest_framework import serializers

from data.models import BlogPost

from .user import SimpleUserSerializer


class BlogPostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer()
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = BlogPost
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "title",
            "tagline",
            "body",
            "published",
            "display_date",
            "author",
            "tags",
        )
