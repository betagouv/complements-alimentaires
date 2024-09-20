from difflib import SequenceMatcher

from django.db.models import F

from data.models import Ingredient, IngredientStatus, Microorganism, Plant
from data.models.substance import Substance, SubstanceType


def search_elements(query, deduplicate=False, exclude_not_authorized=False, exclude_vitamines_minerals=False):
    # Les plantes non autorisées peuvent être ajoutées en infimes quantités dans les elixirs
    # elles sont donc systématiquement renvoyées
    plants = _get_plants(query, deduplicate, exclude_not_authorized=False)
    microorganisms = _get_microorganisms(query, deduplicate, exclude_not_authorized)
    ingredients = _get_ingredients(query, deduplicate, exclude_not_authorized)
    substances = _get_substances(query, deduplicate, exclude_not_authorized, exclude_vitamines_minerals)

    results = plants + microorganisms + ingredients + substances
    results.sort(key=lambda x: SequenceMatcher(None, x.autocomplete_match, query).ratio(), reverse=True)

    return results


def _get_plants(query, deduplicate, exclude_not_authorized):
    plant_qs = (
        Plant.up_to_date_objects.filter(name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("name"))
    )
    plant_synonym_qs = (
        Plant.up_to_date_objects.filter(plantsynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("plantsynonym__name"))
    )
    return _get_element_list(plant_qs, plant_synonym_qs, deduplicate, exclude_not_authorized)


def _get_microorganisms(query, deduplicate, exclude_not_authorized):
    microorganism_qs = (
        Microorganism.up_to_date_objects.filter(name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("name"))
    )
    microorganism_synonym_qs = (
        Microorganism.up_to_date_objects.filter(microorganismsynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("microorganismsynonym__name"))
    )
    return _get_element_list(microorganism_qs, microorganism_synonym_qs, deduplicate, exclude_not_authorized)


def _get_ingredients(query, deduplicate, exclude_not_authorized):
    ingredient_qs = (
        Ingredient.up_to_date_objects.filter(name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("name"))
    )
    ingredient_synonym_qs = (
        Ingredient.up_to_date_objects.filter(ingredientsynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("ingredientsynonym__name"))
    )
    return _get_element_list(ingredient_qs, ingredient_synonym_qs, deduplicate, exclude_not_authorized)


def _get_substances(query, deduplicate, exclude_not_authorized, exclude_vitamines_minerals=False):
    substance_qs = (
        Substance.up_to_date_objects.filter(name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("name"))
    )
    substance_synonym_qs = (
        Substance.up_to_date_objects.filter(substancesynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("substancesynonym__name"))
    )
    if exclude_vitamines_minerals:
        substance_qs = substance_qs.exclude(substance_types__overlap=[SubstanceType.VITAMIN, SubstanceType.MINERAL])
        substance_synonym_qs = substance_synonym_qs.exclude(
            substance_types__overlap=[SubstanceType.VITAMIN, SubstanceType.MINERAL]
        )

    return _get_element_list(substance_qs, substance_synonym_qs, deduplicate, exclude_not_authorized)


def _get_element_list(q1, q2, deduplicate, exclude_not_authorized):
    if exclude_not_authorized:
        q1 = q1.exclude(status=IngredientStatus.NOT_AUTHORIZED)
        q2 = q2.exclude(status=IngredientStatus.NOT_AUTHORIZED)
    merged_qs = q1.union(q2)
    elements = list(merged_qs)

    if not deduplicate:
        return elements

    # On ne peut pas utiliser distinct après un `union` donc on le fait directement sur le tableau
    unique_list = []
    for element in elements:
        if not list(filter(lambda x: x.id == element.id, unique_list)):
            unique_list.append(element)
    return unique_list
