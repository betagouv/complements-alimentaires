from django.contrib.auth import get_user_model

from rest_framework import serializers

from .user import SimpleUserSerializer

User = get_user_model()


# TODO: only change usage for view in question
class HistoricalRecordSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    history_date = serializers.DateTimeField()
    history_change_reason = serializers.CharField()

    def get_user(self, obj):
        users = User.objects.filter(id=obj.history_user_id)
        if obj.history_user_id and users.exists():
            return SimpleUserSerializer(users.first()).data


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        dvs = HistoricalRecordSerializer(data, many=True).data
        return super().to_representation(dvs)
