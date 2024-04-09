from .user import User  # noqa: F401
from .roles import BaseRole, Declarant, CompanySupervisor  # noqa: F401
from .blogpost import BlogPost  # noqa: F401
from .webinar import Webinar  # noqa: F401
from .company import Company  # noqa: F401

# Elements specific models
from .ingredient import Ingredient, IngredientSynonym  # noqa: F401
from .microorganism import Microorganism, MicroorganismSynonym  # noqa: F401
from .plant import Plant, PlantSynonym, PlantPart, PlantFamily, Part  # noqa: F401
from .substance import Substance, SubstanceSynonym  # noqa: F401
from .population import Population  # noqa: F401
from .condition import Condition  # noqa: F401
from .effect import Effect  # noqa: F401
from .galenic_formulation import GalenicFormulation  # noqa: F401
from .unit import SubstanceUnit  # noqa: F401
from .declaration import (  # noqa: F401
    Declaration,  # noqa: F401
    DeclaredPlant,  # noqa: F401
    DeclaredMicroorganism,  # noqa: F401
    DeclaredIngredient,  # noqa: F401
    DeclaredSubstance,  # noqa: F401
    ComputedSubstance,  # noqa: F401
    Attachment,  # noqa: F401
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

DECLARATION_MODELS = [Condition, Effect, GalenicFormulation, Population, SubstanceUnit]
