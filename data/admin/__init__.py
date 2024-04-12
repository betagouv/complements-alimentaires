from django.contrib import admin

from data.admin.abstract_admin import IngredientAdminHistorisableChangedFields
from data.models import Ingredient, PlantFamily, PlantPart

from .blogpost import BlogPostAdmin
from .company import CompanyAdmin
from .condition import Condition
from .effect import Effect
from .microorganism import MicroorganismAdmin
from .plant import PlantAdmin
from .population import Population
from .roles import CompanySupervisorAdmin, DeclarantAdmin
from .substance import SubstanceAdmin
from .user import UserAdmin
from .webinar import WebinarAdmin


@admin.register(Ingredient)
class IngredientAdmin(IngredientAdminHistorisableChangedFields):
    pass


@admin.register(PlantPart)
class PlantPartAdmin(IngredientAdminHistorisableChangedFields):
    pass


@admin.register(PlantFamily)
class PlantFamilyAdmin(IngredientAdminHistorisableChangedFields):
    pass


def get_admin_header():
    return "Compl'Alim"


admin.site.site_header = get_admin_header()
admin.site.site_title = get_admin_header()
