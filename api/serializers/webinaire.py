from rest_framework import serializers
from data.models import Webinaire


class WebinaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinaire
        fields = (
            "id",
            "title",
            "tagline",
            "start_date",
            "end_date",
            "link",
        )
