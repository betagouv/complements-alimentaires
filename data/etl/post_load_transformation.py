import logging

from django.db import transaction
from django.db.models import Q, TextField, Transform

from ..models import Ingredient, IngredientStatus, Substance
from .utils import update_or_create_object


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
    qs_with_CAS = Ingredient.objects.filter(
        name__lower__in=Substance.objects.exclude(Q(is_obsolete=True) | Q(cas_number="")).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon substance qui est un métabolite de plante sont supprimés
    qs_metabolite = Ingredient.objects.filter(
        name__lower__in=Substance.objects.exclude(Q(is_obsolete=True) | Q(plant=None)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ase sont des enzyme
    enzym_suffix = ["ase$"]

    qs_enzym = Ingredient.objects.filter(
        name__lower__regex="|".join(enzym_suffix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(enzym_suffix)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ose/oses sont des glucides
    ose_suffix = ["ose$", "oses$"]

    qs_ose = Ingredient.objects.filter(
        name__lower__regex="|".join(ose_suffix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(ose_suffix)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom se termine par -ate/-ates sont des bases conjuguées
    # Une base conjuguée contient un acide et ses sels. L'acide est considéré comme substance mais pas sa base conjuguée ?
    ate_suffix = ["ate$", "ates$"]
    qs_ate = Ingredient.objects.filter(
        name__lower__regex="|".join(ate_suffix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(ate_suffix)).values_list(
            "name__lower", flat=True
        ),
    )

    # Les ingrédients qui ont un doublon sustance et dont le nom commence par acide -/acides - sont des substances
    acide_prefix = ["^acide ", "^acides"]
    qs_acide = Ingredient.objects.filter(
        name__lower__regex="|".join(acide_prefix),
        name__lower__in=Substance.objects.filter(name__lower__regex="|".join(acide_prefix)).values_list(
            "name__lower", flat=True
        ),
    )
    ingredients_to_delete = qs_with_CAS | qs_metabolite | qs_enzym | qs_ose | qs_ate | qs_acide
    ingredients_to_delete.update(ca_is_obsolete=True)
    for ingredient in ingredients_to_delete:
        subst_to_keep = Substance.objects.filter(name__lower=ingredient.name.lower())[0]
        new_fields = check_all_fields_are_the_same(object_to_delete=ingredient, object_to_keep=subst_to_keep)
        update_or_create_object(
            Substance,
            object_definition={"id": subst_to_keep.id},
            default_extra_fields=new_fields,
            change_message="Suppression de l'ingrédient doublon",
        )

    return len(ingredients_to_delete)


def delete_substances_that_are_ingredients():
    # TODO Les ingrédient en 3 mots "*ate de *" qui ont un doublon sustance sont des formes d'apport

    # Les substances qui ont un doublon ingrédient et qui commencent par huile*, lait* ou miel sont supprimées
    animal_or_vegetal_product_prefix = ["^huile", "^lait", "^miel", "^beurre", "^hydrolysat", "^cartilage", "^extrait"]
    qs_ingredients = Ingredient.objects.filter(name__lower__regex="|".join(animal_or_vegetal_product_prefix))
    qs_substances = Substance.objects.filter(
        name__lower__regex="|".join(animal_or_vegetal_product_prefix),
        name__lower__in=qs_ingredients.values_list("name__lower", flat=True),
    )

    qs_substances.update(ca_is_obsolete=True)
    for subst in qs_substances:
        ingredient_to_keep = qs_ingredients.filter(name__lower=subst.name.lower())[0]
        new_fields = check_all_fields_are_the_same(object_to_delete=subst, object_to_keep=ingredient_to_keep)
        update_or_create_object(
            Ingredient,
            object_definition={"id": ingredient_to_keep.id},
            default_extra_fields=new_fields,
            change_message="Suppression de la substance doublon",
        )

    return len(qs_substances)


def delete_ingredients_and_substances_that_are_microorganism():
    microorganism_suffix = ["inactivé$", "inactivés$"]
    qs_ingredients = Ingredient.objects.filter(
        name__lower__regex="|".join(microorganism_suffix),
    )

    qs_substances = Substance.objects.filter(
        name__lower__regex="|".join(microorganism_suffix),
    )
    qs_ingredients.update(ca_is_obsolete=True)
    qs_substances.update(ca_is_obsolete=True)

    return len(qs_ingredients) + len(qs_substances)


def check_all_fields_are_the_same(object_to_delete, object_to_keep):
    fields_to_check = ["status", "public_comments", "private_comments"]
    new_fields = {}
    for field_name in fields_to_check:
        object_to_delete_field = getattr(object_to_delete, field_name)
        object_to_keep_field = getattr(object_to_keep, field_name)
        if object_to_delete_field != object_to_keep_field:
            # si le status est différent, log une erreur pour vérification manuelle
            if field_name == "status":
                if not any(
                    status
                    in (
                        IngredientStatus.NO_STATUS,
                        None,
                    )
                    for status in [object_to_delete_field, object_to_keep_field]
                ):
                    logger.error(
                        f"{object_to_delete._meta.model.__name__}:{object_to_delete} et {object_to_keep._meta.model.__name__}:{object_to_keep} sont dupliqués mais ont un status différent. En attente de vérification manuelle"
                    )
                    new_fields[f"ca_{field_name}"] = object_to_delete_field
                else:
                    # si le status est différent mais que la différence n'est pas significative, on ne change rien
                    pass
            else:
                new_fields[f"ca_{field_name}"] = (
                    f"{object_to_keep_field} \n Ancien champ de {object_to_delete._meta.model.__name__} : {object_to_delete_field}"
                )

    return new_fields
