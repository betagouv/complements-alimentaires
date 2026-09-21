from difflib import SequenceMatcher

from django.db.models import CharField, F, Q, TextField

from rest_framework import filters

from data.models import Ingredient, IngredientStatus, Microorganism, Plant
from data.models.substance import Substance, SubstanceType


def search_elements(query, deduplicate=False, exclude_not_authorized=False, keep_only_standalone_usable=False):
    term = query["term"]
    query_type = query.get("type")
    # Les plantes non autorisées peuvent être ajoutées en infimes quantités dans les elixirs
    # elles sont donc systématiquement renvoyées
    plants = (
        _get_plants(term, deduplicate, exclude_not_authorized=False) if not query_type or query_type == "plant" else []
    )
    microorganisms = (
        _get_microorganisms(term, deduplicate, exclude_not_authorized)
        if not query_type or query_type == "microorganism"
        else []
    )
    ingredients = (
        _get_ingredients(term, deduplicate, exclude_not_authorized)
        if not query_type or query_type == "other-ingredient"
        else []
    )
    substances = (
        _get_substances(term, deduplicate, exclude_not_authorized, keep_only_standalone_usable)
        if not query_type or query_type == "substance"
        else []
    )

    results = plants + microorganisms + ingredients + substances
    results.sort(key=lambda x: SequenceMatcher(None, x.autocomplete_match, term).ratio(), reverse=True)

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


def _get_substances(query, deduplicate, exclude_not_authorized, keep_only_standalone_usable=False):
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
    if keep_only_standalone_usable:
        substance_qs = substance_qs.filter(substance_types__contains=[SubstanceType.BIOACTIVE_SUBSTANCE])
        substance_synonym_qs = substance_synonym_qs.filter(
            substance_types__contains=[SubstanceType.BIOACTIVE_SUBSTANCE]
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


class UnaccentSearchFilter(filters.SearchFilter):
    """
    Ce filtre ajoute automatiquement le modificateur "unaccent" aux champs de recherche pertinents
    (çad CharField et TextField).
    """

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        search_fields = self.get_search_fields(view, request)

        if not search_terms or not search_fields:
            return queryset

        orm_lookups = []
        for search_term in search_terms:
            for search_field in search_fields:
                field = self.get_field_from_path(queryset.model, search_field)
                ignore_accents = isinstance(field, (CharField, TextField))
                updated_search = (
                    Q(**{f"{search_field}__unaccent__icontains": search_term})
                    if ignore_accents
                    else Q(**{f"{search_field}__icontains": search_term})
                )
                orm_lookups.append(updated_search)

        if orm_lookups:
            return queryset.filter(self.get_q_objects(orm_lookups))
        return queryset

    def get_field_from_path(self, model, path):
        parts = path.split("__")
        field = None
        for part in parts:
            field = model._meta.get_field(part)
            model = field.related_model if hasattr(field, "related_model") else None
        return field

    def get_q_objects(self, orm_lookups):
        combined_lookup = orm_lookups[0]
        for lookup in orm_lookups[1:]:
            combined_lookup |= lookup
        return combined_lookup
