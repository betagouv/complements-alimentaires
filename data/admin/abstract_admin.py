from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin


class IngredientAdminHistorisableChangedFields(SimpleHistoryAdmin):
    history_list_display = ["changed_fields"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    @admin.display(ordering="status__name", description="statut")
    def get_status(self, obj):
        if obj.status:
            return obj.status.name
        else:
            return None
