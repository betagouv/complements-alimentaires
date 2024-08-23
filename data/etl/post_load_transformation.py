from django.db.models import Q, TextField, Transform

# from simple_history.utils import update_change_reason
from ..models import Ingredient, Substance


class LowerValue(Transform):
    lookup_name = "lower"
    function = "LOWER"


TextField.register_lookup(LowerValue)


# TODO : générer un mapping des doublons pour la conversion future des CA déclarés


def substance_ingredient_deduplication():
    """Transformation post-loading"""
    # extract des doublons
    delete_ingredient_that_are_substances()
    # delete_substances_that_are_ingredients()
    # transform_duplicated_substances_into_synonyms()
    # indique le nombre de doublons supprimés


def delete_ingredient_that_are_substances():
    # Les ingrédients qui ont un doublon substance avec un n° CAS sont supprimés
    # les ingredients qui ont une substance associée
    # * et qui a un numero CAS
    Ingredient.objects.filter(
        is_obsolete=False,
        name__lower__in=Substance.objects.exclude(Q(is_obsolete=True) | Q(cas_number="")).values_list(
            "name__lower", flat=True
        ),
    ).update(ca_is_obsolete=True)

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ose/oses sont des glucides
    ose_suffix = ["ose$", "oses$"]

    Ingredient.objects.filter(
        is_obsolete=False,
        name__lower__regex="|".join(ose_suffix),
        name__lower__in=Substance.objects.filter(
            is_obsolete=False, name__lower__regex="|".join(ose_suffix)
        ).values_list("name__lower", flat=True),
    ).update(ca_is_obsolete=True)

    # Les ingrédient en 3 mots "*ate de *" qui ont un doublon sustance sont des formes d'apport

    # TODO : Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ate/-ates sont des bases conjuguées
    # Une base conjuguée contient un acide et ses sels. L'acide est considéré comme substance mais pas sa base conjuguée ?
    ate_suffix = ["ate$", "ates$"]
    Ingredient.objects.filter(
        is_obsolete=False,
        name__lower__regex="|".join(ate_suffix),
        name__lower__in=Substance.objects.filter(
            is_obsolete=False, name__lower__regex="|".join(ate_suffix)
        ).values_list("name__lower", flat=True),
    ).update(ca_is_obsolete=True)

    # Les ingrédients qui ont un doublon sustance et dont le nom commence par acide -/acides - sont des substances
    acide_prefix = ["^acide ", "^acides"]
    Ingredient.objects.filter(
        is_obsolete=False,
        name__lower__regex="|".join(acide_prefix),
        name__lower__in=Substance.objects.filter(
            is_obsolete=False, name__lower__regex="|".join(acide_prefix)
        ).values_list("name__lower", flat=True),
    ).update(ca_is_obsolete=True)


# def delete_substances_that_are_ingredients():

# def substance_is_plant_metabolite()


# def soft_delete(object, model):
#     model_object, created = model.objects.update_or_create(**object_definition, defaults=default_extra_fields)

#     model.ca_is_obsolete = True
#     update_change_reason(model_object, change_message)
