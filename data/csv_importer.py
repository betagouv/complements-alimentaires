import csv
import logging
import os

from django.db.models import ForeignKey, ManyToManyField, TextField, CharField, FloatField, IntegerField

from .exceptions import CSVFileError

# Import the model
from .models.ingredient import Ingredient, IngredientSynonym
from .models.microorganism import Microorganism
from .models.plant import Plant, PlantPart, PlantSynonym, PlantFamily, Part
from .models.population import Population
from .models.substance import Substance, SubstanceSynonym

logger = logging.getLogger(__name__)


# Modèles pour recevoir l'import des données des fichier csv
CSV_TO_MODEL_MAPPING = {
    "REF_ICA_INGREDIENT_AUTRE.csv": Ingredient,
    "REF_ICA_MICRO_ORGANISME.csv": Microorganism,
    "REF_ICA_PARTIE_PLANTE.csv": PlantPart,
    "REF_ICA_PLANTE.csv": Plant,
    "REF_ICA_SUBSTANCE_ACTIVE.csv": Substance,
    "POPULATION.csv": Population,
    # 'OBJECTIF.CSV': Objectif,
    # 'FICHIERA_RECUPERER.CSV': PlantFamily,
    # Les fichiers csv avec les Foreign Keys
    "REF_ICA_INGREDIENT_AUTRE_SYNONYME.csv": IngredientSynonym,
    "REF_ICA_PLANTE_SYNONYME.csv": PlantSynonym,
    "REF_ICA_SUBSTANCE_ACTIVE_SYNONYME.csv": SubstanceSynonym,
    # Les csv avec les relations ManyToMany
    "REF_ICA_AUTREING_SUBSTACTIVE.csv": Ingredient,
    "REF_ICA_PLANTE_SUBSTANCE.csv": Plant,
    "REF_ICA_MOORG_SUBSTANCE.csv": "à récuperer",
    "REF_ICA_PARTIE_PL_A_SURVEILLER.csv": Part,
    "REF_ICA_PARTIE_UTILE.csv": Plant,
}

# Le fichier REF_ICA_PARTIE_PL_A_SURVEILLER n'est pas traité comme une relation car il correspond à un model à part entière
RELATION_CSV = ["REF_ICA_AUTREING_SUBSTACTIVE.csv", "REF_ICA_PLANTE_SUBSTANCE.csv", "REF_ICA_PARTIE_UTILE.csv"]

# Établi le préfix des champs du csv
CSV_TO_TABLE_PREFIX_MAPPING = {
    "REF_ICA_INGREDIENT_AUTRE.csv": "INGA",
    "REF_ICA_MICRO_ORGANISME.csv": "MORG",
    "REF_ICA_PARTIE_PLANTE.csv": "PPLAN",
    "REF_ICA_PLANTE.csv": "PLTE",
    "REF_ICA_SUBSTANCE_ACTIVE.csv": "SBSACT",
    "REF_ICA_INGREDIENT_AUTRE_SYNONYME.csv": "SYNAO",
    "REF_ICA_PLANTE_SYNONYME.csv": "SYNPLA",
    "REF_ICA_SUBSTANCE_ACTIVE_SYNONYME.csv": "SYNSBSTA",
    # Pour les tables de relation on garde le prefix correspondant au modèle dans lequel les données vont être importées
    "REF_ICA_AUTREING_SUBSTACTIVE.csv": "INGA",
    "REF_ICA_PLANTE_SUBSTANCE.csv": "PLTE",
    "REF_ICA_PARTIE_PL_A_SURVEILLER.csv": "",
    "REF_ICA_PARTIE_UTILE.csv": "PLTE",
    "POPULATION.csv": "",
    # "FAMPL"
}

PREFIX_TO_MODEL_MAPPINT = {
    "INGA": Ingredient,
    "MORG": Microorganism,
    "PPLAN": PlantPart,
    "PLTE": Plant,
    "SBSACT": Substance,
    "SYNAO": IngredientSynonym,
    "SYNPLA": PlantSynonym,
    "SYNSBSTA": SubstanceSynonym,
    "FAMPL": PlantFamily,
}

# Établi les suffix des champ des csv correspondant aux champs des modèles Django
DJANGO_FIELD_NAME_TO_CSV_FIELD_NAME_MAPPING = {
    # Les champs simples
    "name": ["LIBELLE", "ESPECE"],
    "name_en": ["LIBELLE_EN"],
    "is_obsolete": ["OBSOLET"],
    "public_comments": ["COMMENTAIRE_PUBLIC"],
    "private_comments": ["COMMENTAIRE_PRIVE"],
    "observation": ["OBSERVATION"],
    "description": ["DESCRIPTION"],
    "cas_number": ["NUMERO_CAS"],
    "einec_number": ["NUM_EINECS"],
    "source": ["SOURCE"],
    "must_specify_quantity": ["QUANTITE_ARENSEIGNER"],
    "min_quantity": ["QTE_MIN"],
    "max_quantity": ["QTE_MAX"],
    "nutritional_reference": ["APPORT_REF"],
    "genre": ["GENRE"],
    "min_age": ["AGE_MIN"],
    "max_age": ["AGE_MAX"],
    "is_defined_by_anses": ["CATEGORIE_ANSES"],
    # Les champs ForeignKey (synonymes)
    "standard_name": ["SBSACT_IDENT", "PLTE_IDENT", "INGA_IDENT", "MORG_IDENT"],
    "family": ["FAMPL_IDENT"],
    "plant": ["PLTE_IDENT"],
    "plantpart": ["PPLAN_IDENT"],
    # Les champs ManyToMany
    "substances": ["SBSACT_IDENT"],
    "plant_parts": ["PPLAN_IDENT"],
}

# Ces champs sont remplis automatiquement et ne sont pas recherchés dans les fichiers csv
AUTOMATICALLY_FILLED = ["id", "siccrf_id", "creation_date", "modification_date", "missing_import_data"]


def import_csv(csv_filepath):
    csv_filename = os.path.basename(csv_filepath)
    if not csv_filename.endswith(".csv"):
        msg = f"'{csv_filename}' n'est pas un fichier csv."
        raise CSVFileError(msg)
    try:
        model = _get_model_from_csv_name(csv_filename)
    except KeyError as e:
        raise CSVFileError(f"Ce nom de fichier ne ressemble pas à ceux attendus : {e}")

    with open(csv_filepath, mode="rb") as csv_file:
        try:
            csv_string = csv_file.read().decode("utf-8-sig")
        except UnicodeDecodeError as e:
            raise CSVFileError(f"'{csv_filename}' n'est pas un fichier unicode.", e)
        try:
            csv_lines = csv_string.splitlines()
            dialect = csv.Sniffer().sniff(csv_lines[0])
        except csv.Error as e:
            raise CSVFileError(f"'{csv_filename}' n'est pas un fichier csv.", e)

        csvreader = csv.DictReader(csv_lines, dialect=dialect)

        logger.info(f"Import de {csv_filename} dans le modèle {model.__name__} en cours.")
        is_relation = True if csv_filename in RELATION_CSV else False
        nb_row, nb_created, updated_models = _import_csv_to_model(
            csv_reader=csvreader, csv_filename=csv_filename, model=model, is_relation=is_relation
        )
        logger.info(
            f"Import de {csv_filename} dans le modèle {model.__name__} terminé : {nb_row} objets importés, {nb_created} objets créés."
        )
    updated_models.add(model)

    return updated_models


def _get_model_from_csv_name(csv_filename):
    return CSV_TO_MODEL_MAPPING[csv_filename]


def _import_csv_to_model(csv_reader, csv_filename, model, is_relation=False):
    nb_line_in_success = 0
    nb_objects_created = 0
    linked_models = set()
    csv_fieldnames = csv_reader.fieldnames
    django_fields_to_column_names = _create_django_fields_to_column_names_mapping(model, csv_fieldnames, csv_filename)
    for row in csv_reader:
        object_definition = {}
        for field, column_name in django_fields_to_column_names.items():
            if not isinstance(field, ForeignKey) and not isinstance(field, ManyToManyField):
                # cas d'un champ simple avec une valeur
                value = row.get(column_name)
                object_definition[field.name] = _clean_value(value, field)
            else:
                # cas d'un champ clé étrangère vers un autre modèle
                foreign_key_id = row.get(column_name)
                try:
                    linked_model = _get_linked_model(column_name)
                    linked_models.add(linked_model)
                    object_definition[field.name] = _get_update_or_create_related_object(linked_model, foreign_key_id)
                except KeyError as e:
                    logger.warning(f"Il n'y a pas de modèle défini pour cette table : {e}")

        # ici, c'est un csv correspondant à une relation complexe (stockée dans un Model spécifique) qui est importée
        if model == Part:
            default_extra_fields = {"must_be_monitored": True}
            object_with_history, created = model.objects.update_or_create(
                **object_definition, defaults=default_extra_fields
            )
        else:
            primary_key = _get_primary_key_label(csv_filename)
            if is_relation:
                # seul le champ correspondant à la relation est mis à jour
                # il n'y a que ce champ dans object_definition
                field_name = list(object_definition)[0]
                instance = _get_update_or_create_related_object(model, row.get(primary_key))
                field_to_update = getattr(instance, field_name)
                nb_elem_in_field = len(field_to_update.all())
                field_to_update.add(object_definition[field_name])
                created = len(field_to_update.all()) != nb_elem_in_field
            else:
                # c'est le csv d'un Model qui est importé
                # le champ `missing_import_data` devient False
                object_definition["missing_import_data"] = False
                object_with_history, created = model.objects.update_or_create(
                    siccrf_id=row.get(primary_key), defaults=object_definition
                )

        nb_objects_created += created
        nb_line_in_success += 1
    return nb_line_in_success, nb_objects_created, linked_models


def _get_model_fields_to_complete(model):
    "Returns all fields(including many-to-many and foreign key) except non editable fields"
    model_fields = model._meta.get_fields()
    # le flag concrete indique les champs qui ont une colonne associée
    return [field for field in model_fields if field.concrete and field.name not in AUTOMATICALLY_FILLED]


def _get_column_name(field_name, csv_fields_in_header, csv_filename, prefixed=True):
    csv_field_names = DJANGO_FIELD_NAME_TO_CSV_FIELD_NAME_MAPPING[field_name]
    if prefixed:
        prefix = CSV_TO_TABLE_PREFIX_MAPPING[csv_filename]
        csv_field_names = [f"{prefix}_{csv_field_name}" for csv_field_name in csv_field_names]
        csv_field_names = [name.removeprefix("_") for name in csv_field_names]
    try:
        csv_field_name = list(set(csv_field_names) & set(csv_fields_in_header))[0]
    except IndexError:
        raise NameError(f"{csv_field_names} n'est pas disponible.")
    return csv_field_name


def _get_linked_model(column_name):
    """
    Récupération du modèle correspondante au nom de colonne d'une clé étrangère
    """
    if not column_name.endswith("IDENT"):
        logger.error(f"{column_name} n'est pas une colonne contenant une clé étrangère.")
        return
    else:
        foreign_key_prefix = column_name.split("_")[0]
        model = PREFIX_TO_MODEL_MAPPINT[foreign_key_prefix]
        return model


def _get_primary_key_label(csv_filename):
    prefix = CSV_TO_TABLE_PREFIX_MAPPING[csv_filename]
    return f"{prefix}_IDENT".removeprefix("_")


def _create_django_fields_to_column_names_mapping(model, csv_fieldnames, csv_filename):
    """
    Creation du mapping entre les nom de champs des modèles django et les nom de colonnes dans les csv
    """
    django_fields = _get_model_fields_to_complete(model)
    django_fields_to_column_names = {}
    missing_fields = []
    for field in django_fields:
        # cas particulier du champ `must_be_monitored`
        # qui n'existe pas en tant que tel dans les csv SICCRF
        if csv_filename == "REF_ICA_PARTIE_PL_A_SURVEILLER.csv" and field.name == "must_be_monitored":
            continue
        # le nom des colonnes contenant les clés étrangères ne sont pas préfixées par le nom de la table
        prefixed = False if isinstance(field, ForeignKey) or isinstance(field, ManyToManyField) else True
        try:
            column_name = _get_column_name(field.name, csv_fieldnames, csv_filename, prefixed=prefixed)
            django_fields_to_column_names[field] = column_name
        except NameError:
            missing_fields.append(field.name)
    if len(missing_fields) > 0:
        logger.warning(f"Ces champs n'existent pas dans le csv' : {missing_fields}")
    return django_fields_to_column_names


def _clean_value(value, field):
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


def _get_update_or_create_related_object(model, id):
    """
    Indépendamment de l'ordre dans lequel les fichiers sont importés,
    les objets sont créés avec seulement leur id s'ils existent dans un fichier relation
    mais n'existent pas encore.
    """
    try:
        return model.objects.get(siccrf_id=id)
    except model.DoesNotExist as e:
        logger.warning(f"Création de l'id {id}, qui n'existait pas encore dans {e}.")
        linked_obj, _ = model.objects.update_or_create(siccrf_id=id, defaults={"name": ""})
        return linked_obj
