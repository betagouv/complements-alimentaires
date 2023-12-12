import logging

import csv
import os

# Import the model
from .models.ingredient import Ingredient, IngredientSynonym
from .models.microorganism import Microorganism  # , MicroorganismSynonym
from .models.plant import Plant, PlantPart, PlantSynonym
from .models.population import Population
from .models.substance import Substance, SubstanceSynonym


# TODO : mettre en place des tests avec des fichiers dummy

logger = logging.getLogger(__name__)

# Établi dans quel modèle les données d'un fichier csv doivent être importées
CSV_TO_MODEL_MAPPING = {
    "REF_ICA_INGREDIENT_AUTRE.csv": Ingredient,
    "REF_ICA_INGREDIENT_AUTRE_SYNONYME.csv": IngredientSynonym,
    "REF_ICA_PLANTE_SYNONYME.csv": PlantSynonym,
    "REF_ICA_MICRO_ORGANISME.csv": Microorganism,
    "REF_ICA_PARTIE_PLANTE.csv": PlantPart,
    "REF_ICA_PLANTE.csv": Plant,
    "REF_ICA_SUBSTANCE_ACTIVE.csv": Substance,
    "REF_ICA_SUBSTANCE_ACTIVE_SYNONYME.csv": SubstanceSynonym,
    "POPULATION.CSV": Population,
    # 'OBJECTIF.CSV': 'objectif',
    # 'REF_ICA_AUTREING_SUBSTACTIVE.csv': 'autreing_substactive',
    # 'REF_ICA_PLANTE_SUBSTANCE.csv': 'plante_substance',
    # 'REF_ICA_PARTIE_PL_A_SURVEILLER.csv': 'partie_pl_a_surveiller',
    # 'REF_ICA_PARTIE_UTILE.csv': 'partie_utile',
}

# Établi le préfix des champs du csv
CSV_TO_TABLE_PREFIX_MAPPING = {
    "REF_ICA_INGREDIENT_AUTRE.csv": "INGA",
    "REF_ICA_INGREDIENT_AUTRE_SYNONYME.csv": "SYNAO",
    "REF_ICA_PLANTE_SYNONYME.csv": "SYNPLA",
    "REF_ICA_MICRO_ORGANISME.csv": "MORG",
    "REF_ICA_PARTIE_PLANTE.csv": "PPLAN",
    "REF_ICA_PLANTE.csv": "PLTE",
    "REF_ICA_SUBSTANCE_ACTIVE.csv": "SBSACT",
    "REF_ICA_SUBSTANCE_ACTIVE_SYNONYME.csv": "SYNSBSTA",
}

# Établi les suffix des champ des csv correspondant aux champs des modèles Django
DJANGO_FIELD_NAME_TO_CSV_FIELD_NAME_MAPPING = {
    "name": "LIBELLE",
    "name_en": "LIBELLE_EN",
    "is_obsolete": "OBSOLET",
    "public_comments": "COMMENTAIRE_PUBLIC",
    "private_comments": "COMMENTAIRE_PRIVE",
    "observation": "OBSERVATION",
    "description": "DESCRIPTION",
    "cas_number": "NUMERO_CAS",
    "einec_number": "NUM_EINECS",
    "source": "SOURCE",
    "must_specify_quantity": "QUANTITE_ARENSEIGNER",
    "min_quantity": "QTE_MIN",
    "max_quantity": "QTE_MAX",
    "nutritional_reference": "APPORT_REF",
    # substances
    # ingredient
    # family
    # useful_parts
    # plant
    # genre
    # microorganism
}


def _get_model_from_csv_name(csv_filename):
    return CSV_TO_MODEL_MAPPING[csv_filename]


def _get_field_to_column_mapping(django_field_names, csv_filename):
    prefix = CSV_TO_TABLE_PREFIX_MAPPING[csv_filename]
    field_to_column_mapping = {}
    for field in django_field_names:
        csv_field_name = DJANGO_FIELD_NAME_TO_CSV_FIELD_NAME_MAPPING[field]
        field_to_column_mapping[field] = f"{prefix}_{csv_field_name}"
    return field_to_column_mapping


def _get_model_fields(model):
    automatically_filled = ["id", "creation_date", "modification_date"]
    return [field.name for field in model._meta.fields if field.name not in automatically_filled]


def import_csv(csv_filepath):
    csv_filename = os.path.basename(csv_filepath)
    if not csv_filename.endswith(".csv"):
        logger.error(f"{csv_filename} n'est pas un fichier csv.")
        return
    else:
        try:
            model = _get_model_from_csv_name(csv_filename)
            django_fields = _get_model_fields(model)
            field_to_column_mapping = _get_field_to_column_mapping(django_fields, csv_filename)
        except KeyError as e:
            logger.error(f"Ce nom de fichier ne ressemble pas à ceux attendus :\n{e}")
        logger.info(f"Import de {csv_filename} dans {model} en cours.")
        with open(csv_filepath) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            nb_row = 0
            for row in csv_reader:
                object_definition = {field: row[column] for field, column in field_to_column_mapping.items()}
                # on utilise un DictReader plutôt qu'un reader, au cas où les colonnes changent
                logger.info(f"Import de {object_definition}")
                _ = model.objects.update_or_create(**object_definition)
                nb_row += 1
            logger.info(f"Import de {csv_filename} dans {model} terminé : {nb_row} objets importés.")


# KeyError
# logger.error("Ne contient pas les colonnes attendues")
