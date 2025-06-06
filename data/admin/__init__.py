from django.contrib import admin

from .user import UserAdmin
from .company import CompanyAdmin
from .blogpost import BlogPostAdmin
from .webinar import WebinarAdmin
from .ingredient import IngredientAdmin
from .substance import SubstanceAdmin
from .plant import PlantAdmin
from .microorganism import MicroorganismAdmin
from .population import Population
from .preparation import Preparation
from .condition import Condition
from .effect import Effect
from .galenic_formulation import GalenicFormulation
from .declaration import DeclarationAdmin
from .solicitation import SupervisionClaimAdmin, CompanyAccessClaim, CollaborationInvitation
from .global_roles import InstructionRoleAdmin
from .error_report import ErrorReportAdmin
from .teleicare_etablissement_to_complalim_company_relation import EtablissementToCompanyRelationAdmin

from data.models import PlantPart, PlantFamily
from simple_history.admin import SimpleHistoryAdmin

from django.contrib.auth.models import Group


@admin.register(PlantPart)
class PlantPartAdmin(SimpleHistoryAdmin):
    pass


@admin.register(PlantFamily)
class PlantFamilyAdmin(SimpleHistoryAdmin):
    pass


def get_admin_header():
    return "Compl'Alim"


admin.site.site_header = get_admin_header()
admin.site.site_title = get_admin_header()
admin.site.unregister(Group)
