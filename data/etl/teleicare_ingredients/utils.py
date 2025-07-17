import logging
import random

from django.db.models import (
    CharField,
    FloatField,
    IntegerField,
    TextField,
)

from bs4 import BeautifulSoup
from simple_history.exceptions import NotHistoricalModelError
from simple_history.utils import update_change_reason

from data.models.ingredient_status import IngredientStatus

logger = logging.getLogger(__name__)


def pre_import_treatments(field, value):
    """
    Fonction dans laquelle se font toutes les modifications des données SICCRF
    pour intégration dans les modèles Compl'Alim :
    * nettoyage de valeurs (trim)
    * transformation de valeurs en d'autres valeurs
    """
    if field.name == "siccrf_max_quantity" and clean_value(value, field) is not None:
        new_fields = {"siccrf_max_quantity": clean_value(value, field), "ca_must_specify_quantity": True}
    elif field.name == "siccrf_status":
        new_fields = {
            "siccrf_status": convert_status(clean_value(value, field)),
        }
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
    """
    match int(value):
        # autorisé
        case 1:
            return IngredientStatus.AUTHORIZED
        # non autorisé
        case 2:
            return IngredientStatus.NOT_AUTHORIZED
        # à inscrire
        case 3:
            return IngredientStatus.AUTHORIZED
        # sans objet
        # ne retourne pas None car cela reviendrait à chercher la valeur 2 dans les GeneratedField avec Coalesce.
        case 4:
            return IngredientStatus.NO_STATUS


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
        if value is None:
            return ""
        else:
            return clean_text(value.strip())
    return value


def clean_text(dirty_text):
    """Certaines données entrées en commentaires publics ou privés notamment contiennent des codes hexa de caractères"""
    # Parse the HTML
    soup = BeautifulSoup(dirty_text, "html.parser")

    # Get the text without HTML tags
    return soup.get_text()


def update_or_create_object(model, object_definition, default_extra_fields, change_message):
    model_object, created = model.objects.update_or_create(**object_definition, defaults=default_extra_fields)
    if len(change_message) > 100:
        logger.warn(f"change_message '{change_message}' too long. Truncating to 100 characters.")
        change_message = change_message[:100]
    try:
        update_change_reason(model_object, change_message)
    except NotHistoricalModelError:
        pass
    return model_object, created


def get_update_or_create_related_object(model, id, change_message):
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
            default_extra_fields={"name": f"${random.randint(0,100)}"},
            change_message=change_message,
        )
        return linked_obj
