from difflib import SequenceMatcher
from django.db.models import F
from data.models import Plant, Microorganism, Ingredient, Substance


def search_elements(query, deduplicate=False):
    plants = _get_plants(query, deduplicate)
    microorganisms = _get_microorganisms(query, deduplicate)
    ingredients = _get_ingredients(query, deduplicate)
    substances = _get_substances(query, deduplicate)

    results = plants + microorganisms + ingredients + substances
    results.sort(key=lambda x: SequenceMatcher(None, x.autocomplete_match, query).ratio(), reverse=True)

    return results


def _get_plants(query, deduplicate):
    plant_qs = Plant.objects.filter(name__unaccent__icontains=query).distinct().annotate(autocomplete_match=F("name"))
    plant_synonym_qs = (
        Plant.objects.filter(plantsynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("plantsynonym__name"))
    )
    return _get_element_list(plant_qs, plant_synonym_qs, deduplicate)


def _get_microorganisms(query, deduplicate):
    microorganism_qs = (
        Microorganism.objects.filter(name__unaccent__icontains=query).distinct().annotate(autocomplete_match=F("name"))
    )
    microorganism_synonym_qs = (
        Microorganism.objects.filter(microorganismsynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("microorganismsynonym__name"))
    )
    return _get_element_list(microorganism_qs, microorganism_synonym_qs, deduplicate)


def _get_ingredients(query, deduplicate):
    ingredient_qs = (
        Ingredient.objects.filter(name__unaccent__icontains=query).distinct().annotate(autocomplete_match=F("name"))
    )
    ingredient_synonym_qs = (
        Ingredient.objects.filter(ingredientsynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("ingredientsynonym__name"))
    )
    return _get_element_list(ingredient_qs, ingredient_synonym_qs, deduplicate)


def _get_substances(query, deduplicate):
    substance_qs = (
        Substance.objects.filter(name__unaccent__icontains=query).distinct().annotate(autocomplete_match=F("name"))
    )
    substance_synonym_qs = (
        Substance.objects.filter(substancesynonym__name__unaccent__icontains=query)
        .distinct()
        .annotate(autocomplete_match=F("substancesynonym__name"))
    )
    return _get_element_list(substance_qs, substance_synonym_qs, deduplicate)


def _get_element_list(q1, q2, deduplicate):
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
