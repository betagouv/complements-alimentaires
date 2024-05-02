from .user import User
from .blogpost import BlogPost
from .webinar import Webinar
from .company import Company, SupervisorRole, DeclarantRole

# Elements specific models
from .ingredient import Ingredient, IngredientSynonym
from .microorganism import Microorganism, MicroorganismSynonym
from .plant import Plant, PlantSynonym, PlantPart, PlantFamily, Part
from .substance import Substance, SubstanceSynonym
from .population import Population
from .condition import Condition
from .effect import Effect
from .galenic_formulation import GalenicFormulation
from .unit import SubstanceUnit
from .status import IngredientStatus
from .declaration import (
    Declaration,
    DeclaredPlant,
    DeclaredMicroorganism,
    DeclaredIngredient,
    DeclaredSubstance,
    ComputedSubstance,
    Attachment,
)
from .solicitation import Solicitation

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

DECLARATION_MODELS = [Condition, Effect, GalenicFormulation, Population]
