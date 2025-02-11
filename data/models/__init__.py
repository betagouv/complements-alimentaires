from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .user import User
from .blogpost import BlogPost
from .webinar import Webinar
from .company import Company, SupervisorRole, DeclarantRole

# Elements specific models
from .ingredient import Ingredient, IngredientSynonym, IngredientSubstanceRelation
from .ingredient_type import IngredientType
from .microorganism import Microorganism, MicroorganismSynonym
from .plant import Plant, PlantSynonym, PlantPart, PlantFamily, Part, PlantSubstanceRelation
from .substance import Substance, SubstanceSynonym, SubstanceType
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
from .teleicare_history.ica_declaration import IcaComplementAlimentaire, IcaDeclaration, IcaVersionDeclaration
from .teleicare_history.ica_etablissement import IcaEtablissement

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
@receiver((m2m_changed), sender=IngredientSubstanceRelation)
@receiver((m2m_changed), sender=PlantSubstanceRelation)
def update_substance_type(sender, instance, action, *args, **kwargs):
    if action in ("post_add", "post_remove", "post_delete"):
        for substance in instance.substances.all():
            substance.substance_types = substance.compute_substance_types()
            Substance.objects.filter(pk=substance.pk).update(substance_types=substance.substance_types)
