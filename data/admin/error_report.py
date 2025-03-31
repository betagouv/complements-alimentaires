from django.contrib import admin

from data.models import ErrorReport


@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    fields = ("email", "message", "author", "status", "element_string")
    readonly_fields = ("email", "message", "author", "element_string")

    list_display = ("truncated_message", "element_string", "status")

    def truncated_message(self, obj):
        return f"{obj.message[:75]}..." if obj.message and len(obj.message) > 30 else obj.message

    @admin.display(description="Ingrédient concerné")
    def element_string(self, obj):
        return obj.element_string
