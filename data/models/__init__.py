from .blogpost import BlogPost
from .company import Company
from .condition import Condition
from .declaration import (
    Attachment,
    ComputedSubstance,
    Declaration,
    DeclaredIngredient,
    DeclaredMicroorganism,
    DeclaredPlant,
    DeclaredSubstance,
)
from .effect import Effect

# Elements specific models
from .ingredient import Ingredient, IngredientSynonym
from .microorganism import Microorganism, MicroorganismSynonym
from .plant import Part, Plant, PlantFamily, PlantPart, PlantSynonym
from .population import Population
from .roles import BaseRole, CompanySupervisor, Declarant
from .substance import Substance, SubstanceSynonym
from .unit import SubstanceUnit
from .user import User
from .webinar import Webinar

ELEMENT_MODELS = [
    Ingredient,
    IngredientSynonym,
    Plant,
    PlantSynonym,
    Microorganism,
    MicroorganismSynonym,
    Substance,
    SubstanceSynonym,
]

DECLARATION_MODELS = [Effect, Condition, Population, SubstanceUnit]
