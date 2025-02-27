from django.contrib.auth import get_user_model

from rest_framework import serializers

from .user import SimpleUserSerializer

User = get_user_model()


class HistoricalRecordSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    history_date = serializers.DateTimeField()
    history_change_reason = serializers.CharField()
    changed_fields = serializers.ListField(child=serializers.CharField())

    def get_user(self, obj):
        users = User.objects.filter(id=obj["history_user_id"])
        if obj["history_user_id"] and users.exists():
            return SimpleUserSerializer(users.first()).data

    def to_representation(self, data):
        return super().to_representation(data)


class HistoricalRecordField(serializers.ListField):
    child = serializers.DictField()

    def to_representation(self, data):
        user = self.context and self.context["request"] and self.context["request"].user
        try:
            is_priviledged_user = user.instructionrole or user.visarole
        except Exception as _:
            is_priviledged_user = False

        if is_priviledged_user:
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
                data_with_changes.append(
                    {
                        "history_date": later_version.history_date,
                        "history_change_reason": later_version.history_change_reason,
                        "history_user_id": later_version.history_user_id,
                        "changed_fields": translated_changed_fields,
                    }
                )
            records = HistoricalRecordSerializer(data_with_changes, many=True).data
            return super().to_representation(records)
        else:
            return super().to_representation(data.values("history_date", "history_change_reason"))
