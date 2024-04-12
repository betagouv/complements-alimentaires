from .user import User
from .roles import BaseRole, Declarant, CompanySupervisor
from .blogpost import BlogPost
from .webinar import Webinar
from .company import Company

# Elements specific models
from .ingredient import Ingredient, IngredientSynonym
from .microorganism import Microorganism, MicroorganismSynonym
from .plant import Plant, PlantSynonym, PlantPart, PlantFamily, Part
from .substance import Substance, SubstanceSynonym
from .population import Population
from .condition import Condition
from .effect import Effect
from .unit import SubstanceUnit
from .declaration import (
    Declaration,
    DeclaredPlant,
    DeclaredMicroorganism,
    DeclaredIngredient,
    DeclaredSubstance,
    ComputedSubstance,
    Attachment,
)


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
