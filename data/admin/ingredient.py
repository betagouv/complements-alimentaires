from django.contrib import admin

from data.models import Ingredient

from .abstract_admin import ElementAdminWithChangeReason


@admin.register(Ingredient)
class IngredientAdmin(ElementAdminWithChangeReason):
    list_display = ("name", "status")
    list_filter = ("is_obsolete", "status")
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_status",
        "siccrf_public_comments",
        "siccrf_private_comments",
    )
    search_fields = ["id", "name"]
