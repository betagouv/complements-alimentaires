from django.db.models import (
    TextField,
    CharField,
    FloatField,
    IntegerField,
)
from simple_history.utils import update_change_reason
from simple_history.exceptions import NotHistoricalModelError


def clean_value(self, value, field):
    if value == "NULL":
        if isinstance(field, TextField) or isinstance(field, CharField):
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
    elif isinstance(field, TextField) or isinstance(field, CharField):
        return value.strip()
    return value


def update_or_create_object(self, model, object_definition, default_extra_fields, change_message):
    model_object, created = model.objects.update_or_create(**object_definition, defaults=default_extra_fields)
    try:
        update_change_reason(model_object, change_message)
    except NotHistoricalModelError:
        pass
    return model_object, created


def get_update_or_create_related_object(self, model, id, csv_filename):
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
