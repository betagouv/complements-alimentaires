from django.db import transaction
from django.db.models import Q, TextField, Transform

# from simple_history.utils import update_change_reason
from ..models import Ingredient, Substance


class LowerValue(Transform):
    lookup_name = "lower"
    function = "LOWER"


TextField.register_lookup(LowerValue)


# TODO : générer un mapping des doublons pour la conversion future des CA déclarés


@transaction.atomic
def substance_ingredient_deduplication():
    """
    Fonction qui déduplique les ingrédients.
    Elle est executée de manière atomique : si une erreur advient aucune opération n'est enregistrée.
    """
    # suppression des doublons
    delete_ingredients_that_are_substances()
    delete_substances_that_are_ingredients()
    delete_ingredients_and_substances_that_are_microorganism()
    # transform_duplicated_substances_into_synonyms()
    # indique le nombre de doublons supprimés


def delete_ingredients_that_are_substances():
    # Les ingrédients qui ont un doublon substance avec un n° CAS sont supprimés
    Ingredient.objects.filter(
        name__lower__in=Substance.objects.exclude(Q(is_obsolete=True) | Q(cas_number="")).values_list(
            "name__lower", flat=True
        ),
    ).update(ca_is_obsolete=True)
    # TODO : check des status
    # TODO : check des commentaires privés/publics

    # Les ingrédients qui ont un doublon substance qui est un métabolite de plante sont supprimés
    Ingredient.objects.filter(
        name__lower__in=Substance.objects.exclude(Q(is_obsolete=True) | Q(plant=None)).values_list(
            "name__lower", flat=True
        ),
    ).update(ca_is_obsolete=True)

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ase sont des enzyme
    enzym_suffix = ["ase$"]

    Ingredient.objects.filter(
        name__lower__regex="|".join(enzym_suffix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(enzym_suffix)).values_list(
            "name__lower", flat=True
        ),
    ).update(ca_is_obsolete=True)

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ose/oses sont des glucides
    ose_suffix = ["ose$", "oses$"]

    Ingredient.objects.filter(
        name__lower__regex="|".join(ose_suffix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(ose_suffix)).values_list(
            "name__lower", flat=True
        ),
    ).update(ca_is_obsolete=True)

    # Les ingrédient en 3 mots "*ate de *" qui ont un doublon sustance sont des formes d'apport

    # TODO : Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ate/-ates sont des bases conjuguées
    # Une base conjuguée contient un acide et ses sels. L'acide est considéré comme substance mais pas sa base conjuguée ?
    ate_suffix = ["ate$", "ates$"]
    Ingredient.objects.filter(
        name__lower__regex="|".join(ate_suffix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(ate_suffix)).values_list(
            "name__lower", flat=True
        ),
    ).update(ca_is_obsolete=True)

    # Les ingrédients qui ont un doublon sustance et dont le nom commence par acide -/acides - sont des substances
    acide_prefix = ["^acide ", "^acides"]
    Ingredient.objects.filter(
        name__lower__regex="|".join(acide_prefix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(acide_prefix)).values_list(
            "name__lower", flat=True
        ),
    ).update(ca_is_obsolete=True)

    # TODO Les ingrédients qui sont des acides aminées dont la liste est connue
    # TODO Les ingrédients qui commencent par L- R- beta- gamma


def delete_substances_that_are_ingredients():
    # Les substances qui ont un doublon ingrédient et qui commencent par huile*, lait* ou miel sont supprimées
    animal_or_vegetal_product_prefix = ["^huile", "^lait", "^miel", "^beurre", "^hydrolysat", "^cartilage", "^extrait"]
    Substance.objects.filter(
        name__lower__regex="|".join(animal_or_vegetal_product_prefix),
        name__lower__in=Ingredient.objects.filter(
            name__lower__regex="|".join(animal_or_vegetal_product_prefix)
        ).values_list("name__lower", flat=True),
    ).update(ca_is_obsolete=True)


def delete_ingredients_and_substances_that_are_microorganism():
    microorganism_suffix = ["inactivé$"]
    Ingredient.objects.filter(
        name__lower__regex="|".join(microorganism_suffix),
    ).update(ca_is_obsolete=True)

    Substance.objects.filter(
        name__lower__regex="|".join(microorganism_suffix),
    ).update(ca_is_obsolete=True)
