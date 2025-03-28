from django.contrib import admin

from data.models import ErrorReport


@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    fields = ("email", "message", "author", "status", "element_string")
    readonly_fields = ("email", "message", "author", "element_string")

    list_display = ("id", "message", "element_string", "status")
