from rest_framework import serializers
from data.models import Webinar


class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = (
            "id",
            "title",
            "tagline",
            "start_date",
            "end_date",
            "link",
        )
