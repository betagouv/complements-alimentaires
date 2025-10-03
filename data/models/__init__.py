from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .user import User
from .blogpost import BlogPost
from .webinar import Webinar
from .company import Company, SupervisorRole, DeclarantRole, ActivityChoices

# Elements specific models
from .ingredient import (
    Ingredient,
    IngredientSynonym,
    IngredientSubstanceRelation,
    IngredientMaxQuantityPerPopulationRelation,
)
from .ingredient_type import IngredientType
from .microorganism import (
    Microorganism,
    MicroorganismSynonym,
    MicroorganismMaxQuantityPerPopulationRelation,
    MicroorganismSubstanceRelation,
)
from .plant import (
    Plant,
    PlantSynonym,
    PlantPart,
    PlantFamily,
    Part,
    PlantSubstanceRelation,
    PlantMaxQuantityPerPopulationRelation,
)
from .substance import Substance, SubstanceSynonym, SubstanceType
from .population import Population
from .condition import Condition
from .effect import Effect
from .galenic_formulation import GalenicFormulation
from .preparation import Preparation
from .unit import SubstanceUnit
from .ingredient_status import IngredientStatus
from .global_roles import InstructionRole, VisaRole, ControlRole, ControlRoleEmail
from .declaration import (
    Declaration,
    DeclaredPlant,
    DeclaredMicroorganism,
    DeclaredIngredient,
    DeclaredSubstance,
    ComputedSubstance,
    Attachment,
    Addable,
)
from .solicitation import SupervisionClaim, CompanyAccessClaim, CollaborationInvitation
from .snapshot import Snapshot
from .teleicare_history.ica_declaration import IcaComplementAlimentaire, IcaDeclaration, IcaVersionDeclaration
from .teleicare_history.ica_etablissement import IcaEtablissement
from .error_report import ErrorReport

import logging

logger = logging.getLogger(__name__)

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
@receiver((m2m_changed), sender=PlantSubstanceRelation)
def update_substance_type(sender, instance, action, model, pk_set, *args, **kwargs):
    if action in ("post_remove", "post_delete", "post_add"):
        if model == Substance:
            for substance in model.objects.filter(pk__in=pk_set):
                substance.update_metabolite_type()
        if model == Plant:
            instance.update_metabolite_type()


@receiver(post_save, sender=User)
def assign_control_role_on_registration(sender, instance, created, **kwargs):
    if created and instance.email:
        if ControlRoleEmail.objects.filter(email__iexact=instance.email).exists():
            ControlRole.objects.get_or_create(user=instance)
            logger.info(f"Rôle de controle crée pour {instance.email}")
