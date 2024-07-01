from django.contrib import admin

from data.models import Declaration, Snapshot


class SnapshotInline(admin.TabularInline):
    model = Snapshot
    can_delete = False
    fields = ("user", "creation_date", "status", "comment")
    readonly_fields = fields
    extra = 0

    def has_add_permission(self, request, object):
        return False


@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "company", "author")
    list_filter = ("status", "company", "author")
    inlines = (SnapshotInline,)
