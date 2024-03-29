from django.contrib import admin

from .user import UserAdmin  # noqa
from .roles import CompanySupervisorAdmin, DeclarantAdmin  # noqa
from .company import CompanyAdmin  # noqa
from .blogpost import BlogPostAdmin  # noqa
from .webinar import WebinarAdmin  # noqa
from .substance import SubstanceAdmin  # noqa
from .plant import PlantAdmin  # noqa
from .population import Population  # noqa
from .condition import Condition  # noqa

from data.models import Ingredient, PlantPart, PlantFamily, Microorganism
from data.admin.abstract_admin import IngredientAdminHistorisableChangedFields


@admin.register(Ingredient)
class IngredientAdmin(IngredientAdminHistorisableChangedFields):
    pass


@admin.register(PlantPart)
class PlantPartAdmin(IngredientAdminHistorisableChangedFields):
    pass


@admin.register(PlantFamily)
class PlantFamilyAdmin(IngredientAdminHistorisableChangedFields):
    pass


@admin.register(Microorganism)
class MicroorganismAdmin(IngredientAdminHistorisableChangedFields):
    pass


def get_admin_header():
    return "Compl'Alim"


admin.site.site_header = get_admin_header()
admin.site.site_title = get_admin_header()
