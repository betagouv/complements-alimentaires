from django.contrib import admin

from data.models import Ingredient
from data.admin.abstract_admin import IngredientAdminHistorisableChangedFields


@admin.register(Ingredient)
class IngredientAdmin(IngredientAdminHistorisableChangedFields):
    list_display = ("name", "status")
    list_filter = ("is_obsolete", "status")
    readonly_fields = (
        "name",
        "is_obsolete",
        "siccrf_public_comments",
        "siccrf_private_comments",
    )
