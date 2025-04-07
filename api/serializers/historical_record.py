from django.contrib.auth import get_user_model

from rest_framework import serializers

from .user import SimpleUserSerializer

User = get_user_model()


class HistoricalRecordSerializer(serializers.Serializer):
    history_date = serializers.DateTimeField()
    changed_fields = serializers.ListField(child=serializers.CharField())
    history_type = serializers.CharField(allow_blank=True, allow_null=True)

    def get_user(self, obj):
        user_id = obj.get("history_user_id")
        if user_id:
            users = User.objects.filter(id=user_id)
            if users.exists():
                return SimpleUserSerializer(users.first()).data

    def to_representation(self, data):
        return super().to_representation(data)


class PriviledgedHistoricalRecordSerializer(HistoricalRecordSerializer):
    user = serializers.SerializerMethodField()
    history_change_reason = serializers.CharField(allow_blank=True, allow_null=True)


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        user = self.context and self.context["request"] and self.context["request"].user
        try:
            is_priviledged_user = user.instructionrole or user.visarole
        except Exception as _:
            is_priviledged_user = False

        data_with_changes = []
        history_list = list(data.all())
        length = len(history_list)
        for idx in range(length):
            later_version = history_list[idx]
            earlier_version = history_list[idx + 1] if idx + 1 < length else None
            changes = later_version.diff_against(earlier_version) if earlier_version else None
            changed_fields = changes.changed_fields if changes else []
            obj_model_meta = type(data.first())._meta
            translated_changed_fields = [obj_model_meta.get_field(f).verbose_name for f in changed_fields]
            history_data = {
                "history_date": later_version.history_date,
                "changed_fields": translated_changed_fields,
                "history_type": later_version.history_type,
            }
            if is_priviledged_user:
                history_data["history_change_reason"] = later_version.history_change_reason
                history_data["history_user_id"] = later_version.history_user_id
            data_with_changes.append(history_data)
        serializer = PriviledgedHistoricalRecordSerializer if is_priviledged_user else HistoricalRecordSerializer
        records = serializer(data_with_changes, many=True).data
        return super().to_representation(records)
