from django.db.models import (
    CharField,
    FloatField,
    IntegerField,
    TextField,
)

from simple_history.exceptions import NotHistoricalModelError
from simple_history.utils import update_change_reason


def pre_import_treatments(field, value):
    """
    Fonction dans laquelle se font toutes les modifications des données SICCRF
    pour intégration dans les modèles Compl'Alim :
    * nettoyage de valeurs (trim)
    * transformation de valeurs en d'autres valeurs
    """

    if field.name == "status":
        new_fields = {field.name: convert_status(clean_value(value, field))}
        # si le status SICCRF correspond à "à inscrire"
        if int(value) == 3:
            new_fields["to_be_entered_in_next_decree"] = 1
    else:
        new_fields = {field.name: clean_value(value, field)}
    return new_fields


def convert_status(value: int) -> int:
    """
    Converti les statuts SICCRF en statuts Compl'Alim
    * à inscrire sera calculé automatiquement à partir de la date d'entrée en base de l'ingrédient
    * sans objet apparaît comme autorisé, car non reliée à une quelconque règlementation
    """
    match int(value):
        # autorisé
        case 1:
            return 1
        # non autorisé
        case 2:
            return 2
        # à inscrire
        case 3:
            return 1
        # sans objet
        case 4:
            return None


def clean_value(value, field):
    if value == "NULL":
        if isinstance(field, (TextField, CharField)):
            return ""
        else:
            return None
    elif isinstance(field, FloatField):
        try:
            # la virgule est considérée dans son usage français des nombres décimaux
            float_value = float(value.replace(",", "."))
            return float_value
        except ValueError:
            if value == "":
                return None
            return value
    elif isinstance(field, IntegerField):
        if value == "":
            return None
        return value
    elif isinstance(field, (TextField, CharField)):
        return value.strip()
    return value


def update_or_create_object(model, object_definition, default_extra_fields, change_message):
    model_object, created = model.objects.update_or_create(**object_definition, defaults=default_extra_fields)
    try:
        update_change_reason(model_object, change_message)
    except NotHistoricalModelError:
        pass
    return model_object, created


def get_update_or_create_related_object(model, id, csv_filename):
    """
    Indépendamment de l'ordre dans lequel les fichiers sont importés,
    les objets sont créés avec seulement leur id s'ils existent dans un fichier relation
    mais n'existent pas encore.
    """
    try:
        return model.objects.get(siccrf_id=id)
    except model.DoesNotExist:
        # logger.warning(f"Création de l'id {id}, qui n'existait pas encore dans {e}.")
        linked_obj, _ = update_or_create_object(
            model,
            object_definition={"siccrf_id": id},
            default_extra_fields={"name": ""},
            change_message=f"Import csv {csv_filename}.",
        )
        return linked_obj
