from django.contrib import admin

from .user import UserAdmin  # noqa
from .roles import CompanySupervisorAdmin, DeclarantAdmin  # noqa
from .company import CompanyAdmin  # noqa
from .blogpost import BlogPostAdmin  # noqa
from .webinar import WebinarAdmin  # noqa
from .substance import SubstanceAdmin  # noqa
from .plant import PlantAdmin  # noqa
from .microorganism import MicroorganismAdmin  # noqa
from .population import Population  # noqa
from .condition import Condition  # noqa

from data.models import Ingredient, PlantPart, PlantFamily
from data.admin.abstract_admin import IngredientAdminWithHistoryChangedFields


@admin.register(Ingredient)
class IngredientAdmin(IngredientAdminWithHistoryChangedFields):
    pass


@admin.register(PlantPart)
class PlantPartAdmin(IngredientAdminWithHistoryChangedFields):
    pass


@admin.register(PlantFamily)
class PlantFamilyAdmin(IngredientAdminWithHistoryChangedFields):
    pass


def get_admin_header():
    return "Compl'Alim"


admin.site.site_header = get_admin_header()
admin.site.site_title = get_admin_header()
