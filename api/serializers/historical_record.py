from django.contrib.auth import get_user_model

from rest_framework import serializers

from .user import SimpleUserSerializer

User = get_user_model()


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
        user = self.context and self.context["request"] and self.context["request"].user
        try:
            is_priviledged_user = user.instructionrole or user.visarole
        except Exception as _:
            is_priviledged_user = False

        if is_priviledged_user:
            records = HistoricalRecordSerializer(data, many=True).data
            return super().to_representation(records)
        else:
            return super().to_representation(data.values("history_date", "history_change_reason"))
