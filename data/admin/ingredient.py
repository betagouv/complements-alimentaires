from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(SimpleHistoryAdmin):
    list_display = ("name", "status")
    list_filter = ("is_obsolete", "status")
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_public_comments",
        "siccrf_private_comments",
    )
