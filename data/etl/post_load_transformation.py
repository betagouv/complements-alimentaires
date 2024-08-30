import logging

from django.db import transaction
from django.db.models import Q, TextField, Transform

# from simple_history.utils import update_change_reason
from ..models import Ingredient, Substance


class LowerValue(Transform):
    lookup_name = "lower"
    function = "LOWER"


TextField.register_lookup(LowerValue)


logger = logging.getLogger(__name__)

# TODO : générer un mapping des doublons pour la conversion future des CA déclarés


@transaction.atomic
def deduplicate_substances_ingredients():
    """
    Fonction qui déduplique les ingrédients.
    Elle est executée de manière atomique : si une erreur advient aucune opération n'est enregistrée.
    """
    nb_duplicate = 0
    # suppression des doublons
    nb_duplicate += delete_ingredients_that_are_substances()
    nb_duplicate += delete_substances_that_are_ingredients()
    nb_duplicate += delete_ingredients_and_substances_that_are_microorganism()
    # TODO transform_duplicated_substances_into_synonyms()
    logger.info(f"{nb_duplicate} doublons supprimés.")


def delete_ingredients_that_are_substances():
    # TODO Les ingrédients qui sont des acides aminées dont la liste est connue
    # TODO Les ingrédients qui commencent par L- R- beta- gamma

    # Les ingrédients qui ont un doublon substance avec un n° CAS sont supprimés
    qs_with_CAS = Ingredient.up_to_date_objects.filter(
        name__lower__in=Substance.up_to_date_objects.exclude(Q(is_obsolete=True) | Q(cas_number="")).values_list(
            "name__lower", flat=True
        ),
    )
    # TODO : check des status
    # TODO : check des commentaires privés/publics

    # Les ingrédients qui ont un doublon substance qui est un métabolite de plante sont supprimés
    qs_metabolite = Ingredient.up_to_date_objects.filter(
        name__lower__in=Substance.up_to_date_objects.exclude(Q(is_obsolete=True) | Q(plant=None)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ase sont des enzyme
    enzym_suffix = ["ase$"]

    qs_enzym = Ingredient.up_to_date_objects.filter(
        name__lower__regex="|".join(enzym_suffix),
        name__lower__in=Substance.up_to_date_objects.filter(name__lower__regex="|".join(enzym_suffix)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ose/oses sont des glucides
    ose_suffix = ["ose$", "oses$"]

    qs_ose = Ingredient.up_to_date_objects.filter(
        name__lower__regex="|".join(ose_suffix),
        name__lower__in=Substance.up_to_date_objects.filter(name__lower__regex="|".join(ose_suffix)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ate/-ates sont des bases conjuguées
    # Une base conjuguée contient un acide et ses sels. L'acide est considéré comme substance mais pas sa base conjuguée ?
    qs_ate = ate_suffix = ["ate$", "ates$"]
    Ingredient.up_to_date_objects.filter(
        name__lower__regex="|".join(ate_suffix),
        name__lower__in=Substance.up_to_date_objects.filter(name__lower__regex="|".join(ate_suffix)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom commence par acide -/acides - sont des substances
    acide_prefix = ["^acide ", "^acides"]
    qs_acide = Ingredient.up_to_date_objects.filter(
        name__lower__regex="|".join(acide_prefix),
        name__lower__in=Substance.up_to_date_objects.filter(name__lower__regex="|".join(acide_prefix)).values_list(
            "name__lower", flat=True
        ),
    )

    ingredients_to_delete = qs_with_CAS | qs_metabolite | qs_enzym | qs_ose | qs_ate | qs_acide
    ingredients_to_delete.update(ca_is_obsolete=True)
    return len(ingredients_to_delete)


def delete_substances_that_are_ingredients():
    # TODO Les ingrédient en 3 mots "*ate de *" qui ont un doublon sustance sont des formes d'apport

    # Les substances qui ont un doublon ingrédient et qui commencent par huile*, lait* ou miel sont supprimées
    animal_or_vegetal_product_prefix = ["^huile", "^lait", "^miel", "^beurre", "^hydrolysat", "^cartilage", "^extrait"]
    qs = Substance.up_to_date_objects.filter(
        name__lower__regex="|".join(animal_or_vegetal_product_prefix),
        name__lower__in=Ingredient.up_to_date_objects.filter(
            name__lower__regex="|".join(animal_or_vegetal_product_prefix)
        ).values_list("name__lower", flat=True),
    )
    qs.update(ca_is_obsolete=True)
    return len(qs)


def delete_ingredients_and_substances_that_are_microorganism():
    microorganism_suffix = ["inactivé$"]
    qs_ingredients = Ingredient.up_to_date_objects.filter(
        name__lower__regex="|".join(microorganism_suffix),
    )

    qs_substances = Substance.up_to_date_objects.filter(
        name__lower__regex="|".join(microorganism_suffix),
    )
    qs_total = qs_ingredients | qs_substances
    qs_total.update(ca_is_obsolete=True)
    return len(qs_total)
