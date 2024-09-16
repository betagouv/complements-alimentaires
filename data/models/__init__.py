from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .user import User
from .blogpost import BlogPost
from .webinar import Webinar
from .company import Company, SupervisorRole, DeclarantRole

# Elements specific models
from .ingredient import Ingredient, IngredientSynonym
from .ingredient_type import IngredientType
from .microorganism import Microorganism, MicroorganismSynonym
from .plant import Plant, PlantSynonym, PlantPart, PlantFamily, Part
from .substance import Substance, SubstanceSynonym
from .population import Population
from .condition import Condition
from .effect import Effect
from .galenic_formulation import GalenicFormulation
from .preparation import Preparation
from .unit import SubstanceUnit
from .ingredient_status import IngredientStatus
from .global_roles import InstructionRole, VisaRole
from .declaration import (
    Declaration,
    DeclaredPlant,
    DeclaredMicroorganism,
    DeclaredIngredient,
    DeclaredSubstance,
    ComputedSubstance,
    Attachment,
)
from .solicitation import SupervisionClaim, CompanyAccessClaim, CollaborationInvitation
from .snapshot import Snapshot

ELEMENT_MODELS = [
    Ingredient,
    IngredientSynonym,
    Plant,
    PlantFamily,
    PlantSynonym,
    Microorganism,
    MicroorganismSynonym,
    Substance,
    SubstanceSynonym,
    IngredientStatus,
    SubstanceUnit,
]

DECLARATION_MODELS = [Condition, Effect, GalenicFormulation, Population, Preparation]


## Signals ici pour éviter les imports récursifs
@receiver((post_save, post_delete), sender=Ingredient)
@receiver((post_save, post_delete), sender=Plant)
def update_substance_type(sender, instance, *args, **kwargs):
    for substance in instance.substances.all():
        substance.substance_types = substance.compute_substance_types()
        Substance.objects.filter(pk=substance.pk).update(substance_types=substance.substance_types)
