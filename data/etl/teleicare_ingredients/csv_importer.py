import csv
import datetime
import logging
import os
import pathlib
from functools import cached_property

from django.db import transaction
from django.db.models import (
    ForeignKey,
    GeneratedField,
    ManyToManyField,
)

from data.etl.exceptions import CSVFileError

# Import the model
from data.models import (
    Condition,
    Effect,
    GalenicFormulation,
    Ingredient,
    IngredientStatus,
    IngredientSynonym,
    Microorganism,
    MicroorganismSynonym,
    Part,
    Plant,
    PlantFamily,
    PlantPart,
    PlantSynonym,
    Preparation,
    Substance,
    SubstanceSynonym,
    SubstanceUnit,
)

from .utils import get_update_or_create_related_object, pre_import_treatments, update_or_create_object

logger = logging.getLogger(__name__)

# Modèles pour recevoir l'import des données des fichier csv
CSV_TO_MODEL_MAPPING = {
    "REF_ICA_INGREDIENT_AUTRE.csv": Ingredient,
    "REF_ICA_MICRO_ORGANISME.csv": Microorganism,
    "REF_ICA_PARTIE_PLANTE.csv": PlantPart,
    "REF_ICA_PLANTE.csv": Plant,
    "REF_ICA_FAMILLE_PLANTE.csv": PlantFamily,
    "REF_ICA_SUBSTANCE_ACTIVE.csv": Substance,
    # "POPULATION_CIBLE.csv": Population,
    "REF_ICA_POPULATION_ARISQUE.csv": Condition,
    "REF_ICA_OBJECTIFS_EFFETS.csv": Effect,
    "REF_ICA_FORME_GALENIQUE.csv": GalenicFormulation,
    "REF_ICA_UNITE.csv": SubstanceUnit,
    "REF_ICA_TYPE_PREPARATION.csv": Preparation,
    # Les fichiers csv avec les Foreign Keys
    "REF_ICA_INGREDIENT_AUTRE_SYNONYME.csv": IngredientSynonym,
    "REF_ICA_PLANTE_SYNONYME.csv": PlantSynonym,
    "REF_ICA_MICROORG_SYNONYME.csv": MicroorganismSynonym,
    "REF_ICA_SUBSTANCE_ACTIVE_SYNONYME.csv": SubstanceSynonym,
    # Les csv avec les relations ManyToMany
    "REF_ICA_AUTREING_SUBSTACTIVE.csv": Ingredient,
    "REF_ICA_PLANTE_SUBSTANCE.csv": Plant,
    "REF_ICA_MICROORG_SUBSTACTIVE.csv": Microorganism,
    "REF_ICA_PARTIE_PL_A_SURVEILLER.csv": Part,
    "REF_ICA_PARTIE_UTILE.csv": Part,
}

# Le fichier REF_ICA_PARTIE_PL_A_SURVEILLER n'est pas traité comme une relation car il correspond à un model à part entière
RELATION_CSV = ["REF_ICA_AUTREING_SUBSTACTIVE.csv", "REF_ICA_PLANTE_SUBSTANCE.csv", "REF_ICA_MICROORG_SUBSTACTIVE.csv"]


class CSVImporter:
    """
    Le csv_importer est déprécié et sera bientôt supprimé

    """

    PREFIX_TO_MODEL_MAPPING = {
        # Pour les tables de relation on garde le prefix correspondant au modèle dans lequel les données vont être importées
        "INGA": Ingredient,
        "MORG": Microorganism,
        "PPLAN": PlantPart,
        "PLTE": Plant,
        "SBSACT": Substance,
        "SYNAO": IngredientSynonym,
        "SYNPLA": PlantSynonym,
        "SYNMO": MicroorganismSynonym,
        "SYNSBSTA": SubstanceSynonym,
        "FAMPL": PlantFamily,
        "UNT": SubstanceUnit,
        "OBJEFF": Effect,
        "FRMGAL": GalenicFormulation,
        "TYPPREP": Preparation,
        "STINGSBS": IngredientStatus,
        "POPRS": Condition,
        # "": Population,
        # "REF_ICA_PARTIE_PL_A_SURVEILLER.csv": "",
        # "REF_ICA_PARTIE_UTILE.csv": "",
    }

    # Établi les suffix des champ des csv correspondant aux champs des modèles Django
    DJANGO_FIELD_NAME_TO_CSV_FIELD_NAME_MAPPING = {
        # Les champs simples
        "name": ["LIBELLE"],  # Pour les Model *Synonym, le champ `name` n'est pas préfixé par `siccrf_`
        "siccrf_name": ["LIBELLE"],
        "siccrf_name_en": ["LIBELLE_EN"],
        "siccrf_is_obsolete": ["OBSOLET"],
        "siccrf_public_comments": ["COMMENTAIRE_PUBLIC"],
        "siccrf_public_comments_en": ["COMMENTAIRE_PUBLIC_EN"],
        "siccrf_private_comments": ["COMMENTAIRE_PRIVE"],
        "siccrf_private_comments_en": ["COMMENTAIRE_PRIVE_EN"],
        "siccrf_observation": ["OBSERVATION"],
        "siccrf_description": ["DESCRIPTION"],
        "ingredient_type": ["TAING_IDENT"],
        # "activity": ["FCTINGR_IDENT"], n'est pas extraite par le CSV Importer car est assignée par type d'ingrédient
        "siccrf_cas_number": ["NUMERO_CAS"],
        "siccrf_einec_number": ["NUM_EINECS"],
        "siccrf_source": ["SOURCE"],
        "siccrf_must_specify_quantity": ["QUANTITE_ARENSEIGNER"],
        "siccrf_nutritional_reference": ["APPORT_REF"],
        "unit": ["UNT_IDENT"],
        "siccrf_genus": ["GENRE"],
        "siccrf_species": ["ESPECE"],
        "min_age": ["AGE_MIN"],
        "max_age": ["AGE_MAX"],
        "is_defined_by_anses": ["CATEGORIE_ANSES"],
        "is_liquid": ["LIQUIDE"],
        "contains_alcohol": ["AVEC_ALCOOL"],
        # Les champs ForeignKey (synonymes)
        "standard_name": ["SBSACT_IDENT", "PLTE_IDENT", "INGA_IDENT", "MORG_IDENT"],
        "siccrf_family": ["FAMPL_IDENT"],
        "plant": ["PLTE_IDENT"],
        "plantpart": ["PPLAN_IDENT"],
        # Les champs ManyToMany
        "substances": ["SBSACT_IDENT"],
        "plant_parts": ["PPLAN_IDENT"],
        "siccrf_status": ["STINGSBS_IDENT"],
    }

    # Ces champs sont remplis automatiquement et ne sont pas recherchés dans les fichiers csv
    AUTOMATICALLY_FILLED = [
        "id",
        "siccrf_id",
        "creation_date",
        "modification_date",
        "missing_import_data",
        "to_be_entered_in_next_decree",
        "substance_types",
        "is_obsolete",
        # Les dernières modification de modèle de données s'éloignent du modèle de données TeleIcare
        # cela rend difficile l'automatisation (via csv_importer) pour remplir les nouveaux champs
        "max_quantities",
    ]
    NEW_FIELDS = ["long_name", "is_risky", "novel_food", "category"]

    def __init__(self, file, model, is_relation=False, mapping=None):
        """Initialise un CSVImporter avec le fichier source, le modèle de destination, etc
        :param file: peut être de type InMemoryUploadedFile ou _io.BufferedReader
        """
        self.file = file
        self.filename = self._check_file_format()
        self.lines, self.dialect = self._check_file_encoding()
        self.reader = csv.DictReader(self.lines, dialect=self.dialect)
        self.model = model
        self.is_relation = is_relation
        self.django_fields_to_csv_column_mapping = (
            mapping if mapping else self._create_django_fields_to_column_names_mapping()
        )
        self.nb_line_in_success = 0
        self.nb_objects_created = 0

    def _check_file_format(self):
        path = pathlib.PurePath(self.file.name)
        if not path.suffix.lower() == ".csv":
            raise CSVFileError(f"'{path.name}' n'est pas un fichier csv.")
        return path.name

    def _check_file_encoding(self):
        """
        2 encoding sont possibles : UTF-8 et UTF-16
        """
        try:
            raw_file = self.file.read()
            csv_string = raw_file.decode("utf-8-sig")
        except UnicodeDecodeError:
            try:
                csv_string = raw_file.decode("utf-16")
            except UnicodeDecodeError as e:
                raise CSVFileError(f"'{self.filename}' n'est pas un fichier unicode.", e)
        try:
            csv_lines = csv_string.splitlines()
            dialect = csv.Sniffer().sniff(csv_lines[0])
        except csv.Error as e:
            raise CSVFileError(f"'{self.filename}' n'est pas un fichier csv.", e)
        return csv_lines, dialect

    @property
    def fields_to_complete(self):
        "Returns all fields(including many-to-many and foreign key) except non editable fields"
        model_fields = self.model._meta.get_fields()
        # le flag concrete indique les champs qui ont une colonne associée
        return [
            field
            for field in model_fields
            if field.concrete
            and field.name not in self.AUTOMATICALLY_FILLED
            and field.name not in self.NEW_FIELDS
            and not field.__class__ == GeneratedField
            and not field.name.startswith("ca_")
            and not field.name == "origin_declaration"
        ]

    @cached_property
    def linked_models(self):
        """
        Récupération des modèles en lien par les champs de type ForeignKey
        """
        column_to_linked_model = {}
        for field, column_name in self.django_fields_to_csv_column_mapping.items():
            if isinstance(field, ForeignKey) or isinstance(field, ManyToManyField):
                column_to_linked_model[column_name] = self.PREFIX_TO_MODEL_MAPPING[column_name.split("_")[0]]
        return column_to_linked_model

    @cached_property
    def prefix(self):
        for a_prefix, a_model in self.PREFIX_TO_MODEL_MAPPING.items():
            if self.model == a_model:
                return a_prefix

    @cached_property
    def primary_key_label(self):
        return f"{self.prefix}_IDENT".removeprefix("_")

    def _create_django_fields_to_column_names_mapping(self):
        """
        Creation du mapping entre les nom de champs des modèles django et les nom de colonnes dans les csv
        """
        django_fields_to_column_names = {}
        missing_fields = []
        for field in self.fields_to_complete:
            # cas particulier des champs `siccrf_must_be_monitored` et `siccrf_is_useful`
            # qui n'existent pas en tant que tel dans les csv SICCRF
            # TODO : ces champs devraient juste être ajoutés à la liste des champs remplis automatiquement ?
            if self.model == Part and field.name in ["siccrf_must_be_monitored", "siccrf_is_useful"]:
                continue
            # le nom des colonnes contenant les clés étrangères ne sont pas préfixées par le nom de la table
            prefixed = not (
                isinstance(field, (ForeignKey, ManyToManyField)) or field.name in ["siccrf_status", "ingredient_type"]
            )
            try:
                column_name = self._get_column_name(field.name, prefixed=prefixed)
                django_fields_to_column_names[field] = column_name
            except NameError:
                missing_fields.append(field.name)
        if len(missing_fields) > 0:
            logger.warning(f"Ces champs n'existent pas dans le csv' : {missing_fields}")
        return django_fields_to_column_names

    def _get_column_name(self, field_name, prefixed=True):
        csv_field_names = self.DJANGO_FIELD_NAME_TO_CSV_FIELD_NAME_MAPPING[field_name]
        if prefixed:
            csv_field_names = [f"{self.prefix}_{csv_field_name}" for csv_field_name in csv_field_names]
            csv_field_names = [name.removeprefix("_") for name in csv_field_names]
        try:
            csv_field_name = list(set(csv_field_names) & set(self.reader.fieldnames))[0]
        except IndexError:
            raise NameError(f"{csv_field_names} n'est pas disponible.")
        return csv_field_name

    def import_csv(self, export_date=datetime.datetime.today()):
        # definition du message de modification pour simple-history
        output_date = export_date.strftime("%d/%m/%Y")
        change_message = f"Intégration des données TELEICARE du {output_date}: {self.filename}."
        for row in self.reader:
            object_definition = {}
            for field, column_name in self.django_fields_to_csv_column_mapping.items():
                if not isinstance(field, ForeignKey) and not isinstance(field, ManyToManyField):
                    # cas d'un champ simple avec une valeur
                    value = row.get(column_name)
                    new_fields = pre_import_treatments(field, value)
                    object_definition.update(new_fields)
                else:
                    # cas d'un champ clé étrangère vers un autre modèle
                    foreign_key_id = row.get(column_name)
                    try:
                        linked_model = self.linked_models[column_name]
                        object_definition[field.name] = get_update_or_create_related_object(
                            linked_model, foreign_key_id, change_message
                        )
                    except KeyError as e:
                        if not column_name.endswith("IDENT"):
                            logger.error(f"{column_name} n'est pas une colonne contenant une clé étrangère.")
                        else:
                            logger.warning(f"Il n'y a pas de modèle défini pour cette table : {e}")

            # ici, c'est un csv correspondant à une relation complexe (stockée dans un Model spécifique)
            # qui est importée
            if self.model == Part:
                default_extra_fields = (
                    {"siccrf_must_be_monitored": True}
                    if self.filename == "REF_ICA_PARTIE_PL_A_SURVEILLER.csv"
                    else {"siccrf_is_useful": True}
                )
                object_with_history, created = update_or_create_object(
                    self.model, object_definition, default_extra_fields, change_message
                )
            else:
                if self.is_relation:
                    # seul le champ correspondant à la relation est mis à jour
                    # il n'y a que ce champ dans object_definition
                    field_name = list(object_definition)[0]
                    instance = get_update_or_create_related_object(
                        self.model, row.get(self.primary_key_label), self.filename
                    )
                    field_to_update = getattr(instance, field_name)
                    nb_elem_in_field = len(field_to_update.all())
                    field_to_update.add(object_definition[field_name])
                    created = len(field_to_update.all()) != nb_elem_in_field
                else:
                    # c'est le csv d'un Model qui est importé
                    object_with_history, created = update_or_create_object(
                        self.model,
                        object_definition={"siccrf_id": row.get(self.primary_key_label)},
                        default_extra_fields=object_definition,
                        change_message=change_message,
                    )

            self.nb_objects_created += created
            self.nb_line_in_success += 1
        return list(self.linked_models.values())


@transaction.atomic
def import_csv_from_filepath(csv_filepath, export_date):
    """Cette fonction utilise la classe CSVImporter en devinant d'abord :
    * si le fichier importé représente une relation
    * le modèle de sortie
    """
    csv_filename = os.path.basename(csv_filepath)
    is_relation = True if csv_filename in RELATION_CSV else False

    try:
        model = _get_model_from_csv_name(csv_filename)
    except KeyError as e:
        raise CSVFileError(f"Ce nom de fichier ne ressemble pas à ceux attendus : {e}")

    with open(csv_filepath, mode="rb") as csv_file:
        csv_importer = CSVImporter(csv_file, model, is_relation=is_relation)
        logger.info(f"Import de {csv_filename} dans le modèle {model.__name__} en cours.")
        updated_models = csv_importer.import_csv(export_date)
        logger.info(
            f"Import de {csv_filename} dans le modèle {model.__name__} terminé : {csv_importer.nb_line_in_success} objets importés, {csv_importer.nb_objects_created} objets créés."
        )

    return updated_models + [model]


def _get_model_from_csv_name(csv_filename):
    return CSV_TO_MODEL_MAPPING[csv_filename]
