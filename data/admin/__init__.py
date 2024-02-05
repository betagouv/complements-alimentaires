from django.contrib import admin

from .user import UserAdmin  # noqa
from .blogpost import BlogPostAdmin  # noqa
from .webinar import WebinarAdmin  # noqa
from .substance import SubstanceAdmin  # noqa
from .plant import PlantAdmin  # noqa
from simple_history.admin import SimpleHistoryAdmin

from data.models import Ingredient, Plant, PlantPart, PlantFamily, Microorganism  # noqa


def get_admin_header():
    return "Compl'Alim"


@admin.register(Ingredient)
class IngredientAdmin(SimpleHistoryAdmin):
    pass


@admin.register(PlantPart)
class PlantPartAdmin(SimpleHistoryAdmin):
    pass


@admin.register(PlantFamily)
class PlantFamilyAdmin(SimpleHistoryAdmin):
    pass


@admin.register(Microorganism)
class MicroorganismAdmin(SimpleHistoryAdmin):
    pass


admin.site.site_header = get_admin_header()
admin.site.site_title = get_admin_header()
