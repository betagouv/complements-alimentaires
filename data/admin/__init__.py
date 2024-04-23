from django.contrib import admin

from .user import UserAdmin
from .roles import CompanySupervisorAdmin, DeclarantAdmin
from .company import CompanyAdmin
from .blogpost import BlogPostAdmin
from .webinar import WebinarAdmin
from .ingredient import IngredientAdmin
from .substance import SubstanceAdmin
from .plant import PlantAdmin
from .microorganism import MicroorganismAdmin
from .population import Population
from .condition import Condition
from .effect import Effect
from .galenic_formulation import GalenicFormulation
from .declaration import DeclarationAdmin

from data.models import PlantPart, PlantFamily
from data.admin.abstract_admin import IngredientAdminHistorisableChangedFields


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
