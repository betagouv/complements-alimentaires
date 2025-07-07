import datetime
import os
from unittest.mock import patch

from django.core.management import call_command
from django.db.models import CharField, FloatField, IntegerField, TextField
from django.test import TestCase

from data.choices import IngredientActivity
from data.etl.exceptions import CSVFileError
from data.etl.teleicare_ingredients.csv_importer import CSVImporter, import_csv_from_filepath
from data.etl.teleicare_ingredients.utils import clean_value
from data.models import (
    Effect,
    GalenicFormulation,
    Ingredient,
    IngredientStatus,
    IngredientType,
    Microorganism,
    Plant,
    PlantFamily,
    PlantPart,
    Substance,
    SubstanceUnit,
)


class CSVImporterTestCase(TestCase):
    TEST_DIR_PATH = "data/tests/files"

    def test_unknown_file_is_not_imported(self):
        file_name = "déclaration_impots_2002.csv"

        with self.assertRaises(CSVFileError) as context:
            import_csv_from_filepath(file_name, datetime.datetime.strptime("2024-05-06", "%Y-%m-%d"))
        self.assertEqual(
            "Ce nom de fichier ne ressemble pas à ceux attendus : 'déclaration_impots_2002.csv'",
            context.exception.message,
        )

    def test_non_csv_file_is_not_imported(self):
        with open(f"{self.TEST_DIR_PATH}/raises_if_not_csv/blank.pdf") as file:
            with self.assertRaises(CSVFileError) as context:
                CSVImporter(file, Plant)
            self.assertEqual("'blank.pdf' n'est pas un fichier csv.", context.exception.message)

    @patch("data.management.commands.load_ingredients.logger")
    def test_raises_if_not_unicode_file(self, mocked_logger):
        test_path = f"{self.TEST_DIR_PATH}/raises_if_not_utf_8_file/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        mocked_logger.error.assert_called_with("'REF_ICA_PLANTE.csv' n'est pas un fichier unicode.")

    def test_accepts_utf_8_and_utf_16_files(self):
        test_path = f"{self.TEST_DIR_PATH}/accepted_encodings/"
        for filepath in os.listdir(test_path):
            with open(os.path.join(test_path, filepath), "rb") as file:
                csv_importer = CSVImporter(file, PlantPart)
                _ = csv_importer.import_csv()
            self.assertEqual(csv_importer.nb_line_in_success, 135)
            self.assertIn(csv_importer.nb_objects_created, [0, 135])

    def test_clean_values(self):
        """TextField should be "" if no value istead of "NULL"
        FloatField should work with french decimal values with a comma
        """
        self.assertEqual(2.5, clean_value("2,5", FloatField()))
        self.assertEqual(2.5, clean_value("2.5", FloatField()))
        self.assertEqual("2,5", clean_value("2,5", IntegerField()))
        self.assertEqual(None, clean_value("NULL", IntegerField()))
        self.assertEqual(None, clean_value("", FloatField()))
        self.assertEqual(None, clean_value("", IntegerField()))
        self.assertEqual("", clean_value("", TextField()))
        self.assertEqual("", clean_value("NULL", TextField()))
        self.assertEqual("", clean_value("NULL", CharField()))
        self.assertEqual("Eloides rhamnosus trulul", clean_value(" Eloides rhamnosus trulul ", CharField()))

    def test_element_models_created(self):
        test_path = f"{self.TEST_DIR_PATH}/element_models_creation/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        self.assertTrue(Plant.objects.filter(siccrf_id=10).exists())
        self.assertTrue(Plant.objects.filter(siccrf_id=11).exists())
        self.assertEqual(len(Plant.objects.all()), 2)

        self.assertTrue(PlantPart.objects.filter(siccrf_id=10).exists())
        self.assertTrue(PlantPart.objects.filter(siccrf_id=20).exists())
        self.assertTrue(PlantPart.objects.filter(siccrf_id=30).exists())
        self.assertEqual(len(PlantPart.objects.all()), 3)

        self.assertTrue(Ingredient.objects.filter(siccrf_id=10).exists())
        self.assertTrue(Ingredient.objects.filter(siccrf_id=11).exists())
        self.assertEqual(len(Ingredient.objects.all()), 2)

        self.assertTrue(Microorganism.objects.filter(siccrf_id=10).exists())
        self.assertEqual(len(Microorganism.objects.all()), 2)

        self.assertTrue(Substance.objects.filter(siccrf_id=10).exists())
        self.assertTrue(Substance.objects.filter(siccrf_id=11).exists())
        self.assertEqual(len(Substance.objects.all()), 2)

        self.assertEqual(len(SubstanceUnit.objects.all()), 5)

    def test_ingredient_models_created(self):
        test_path = f"{self.TEST_DIR_PATH}/declaration_models_creation/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        self.assertTrue(Effect.objects.filter(siccrf_id=1).exists())
        self.assertTrue(Effect.objects.filter(siccrf_id=2).exists())
        self.assertTrue(Effect.objects.filter(siccrf_id=3).exists())
        self.assertTrue(Effect.objects.filter(siccrf_id=35).exists())
        self.assertEqual(len(Effect.objects.all()), 4)

        self.assertTrue(GalenicFormulation.objects.filter(siccrf_id=1).exists())
        self.assertTrue(GalenicFormulation.objects.filter(siccrf_id=5).exists())
        self.assertTrue(GalenicFormulation.objects.filter(siccrf_id=6).exists())
        self.assertEqual(len(GalenicFormulation.objects.all()), 3)

    def test_linked_models_created_even_if_no_corresponding_file(self):
        test_path = f"{self.TEST_DIR_PATH}/element_models_creation/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)
        self.assertTrue(PlantFamily.objects.filter(siccrf_id=6).exists())
        self.assertEqual(PlantFamily.objects.get(siccrf_id=6).name, "")

    def test_import_twice_same_synonym_created_only_once(self):
        test_path = f"{self.TEST_DIR_PATH}/import_twice_same_synonym_created_only_once/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)
        # les lignes doublonnées ne sont pas ajoutées
        self.assertEqual(len(Plant.objects.get(name="Pour les pieds").plantsynonym_set.all()), 4)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").plantsynonym_set.all()), 3)
        # mais les lignes dont l'id est différent sont ajoutées 2 fois
        self.assertEqual(
            len(Plant.objects.get(name="Pour les pieds").plantsynonym_set.filter(name="Chaussure à talons")), 2
        )

    def test_creates_models_with_their_relations(self):
        test_path = f"{self.TEST_DIR_PATH}/creates_models_with_their_relations/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        self.assertEqual(len(Plant.objects.get(name="Pour les pieds").plant_parts.all()), 1)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").plant_parts.all()), 3)

    def test_create_objects_in_relation_if_they_do_not_already_exist(self):
        test_path = f"{self.TEST_DIR_PATH}/create_objects_in_relation_if_they_do_not_already_exist/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        self.assertEqual(len(Plant.objects.get(name="Pour les pieds").plant_parts.all()), 1)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").plant_parts.all()), 4)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").plant_parts.all()), 4)
        first_id = Plant.objects.get(siccrf_id=1)
        self.assertEqual(len(first_id.plant_parts.all()), 1)
        self.assertEqual(first_id.name, "")
        second_id = Plant.objects.get(siccrf_id=2)
        # dans le fichier une ligne de relation est dupliquée
        self.assertEqual(len(second_id.plant_parts.all()), 2)
        self.assertEqual(second_id.name, "")

    def test_plantparts_status_is_not_always_useful(self):
        """
        Il existe des plantparts avec siccrf_is_useful = False et siccrf_must_be_monitored = True
        """
        test_path = f"{self.TEST_DIR_PATH}/create_plants_with_distinct_useful_and_to_be_monitored_parts/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        plants_with_parts = Plant.objects.exclude(plant_parts=None)
        for plant in plants_with_parts:
            all_parts = {part_relation.plantpart.name for part_relation in plant.part_set.all()}
            useful_parts = {
                part_relation.plantpart.name for part_relation in plant.part_set.all() if part_relation.is_useful
            }
            must_be_monitored_parts = {
                part_relation.plantpart.name
                for part_relation in plant.part_set.all()
                if part_relation.must_be_monitored
            }
            self.assertTrue(useful_parts.issubset(all_parts))
            self.assertTrue(must_be_monitored_parts.issubset(all_parts))
            self.assertFalse(useful_parts.issubset(must_be_monitored_parts))
            self.assertFalse(useful_parts.issuperset(must_be_monitored_parts))

    def test_status_import(self):
        """
        Les ingrédients (plante, microorganism, autre ingrédients) et substance peuvent avoir différent status.
        Ce test vérifie que le modèle Status est bien rempli et que les ForeignKey des différents ingrédients/substances
        pointent bien comme convenu vers le bon objet du modèle Status.
        """
        test_path = f"{self.TEST_DIR_PATH}/element_models_creation/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        self.assertEqual(len(Plant.objects.filter(status=IngredientStatus.AUTHORIZED)), 2)
        self.assertEqual(len(Plant.objects.filter(siccrf_status=1)), 2)

        self.assertEqual(len(Microorganism.objects.filter(status=IngredientStatus.AUTHORIZED)), 2)
        self.assertEqual(len(Microorganism.objects.filter(siccrf_status=3)), 0)  # ce status est converti
        self.assertEqual(len(Microorganism.objects.filter(siccrf_status=1)), 2)
        self.assertEqual(len(Microorganism.objects.filter(to_be_entered_in_next_decree=True)), 2)

        self.assertEqual(len(Ingredient.objects.filter(status=IngredientStatus.NO_STATUS)), 2)
        self.assertEqual(len(Ingredient.objects.filter(siccrf_status=4)), 0)  # ce status est converti
        self.assertEqual(len(Ingredient.objects.filter(siccrf_status=3)), 2)
        self.assertEqual(len(Ingredient.objects.filter(status=IngredientStatus.AUTHORIZED)), 0)

        self.assertEqual(len(Substance.objects.filter(status=IngredientStatus.NOT_AUTHORIZED)), 2)
        self.assertEqual(len(Substance.objects.filter(siccrf_status=2)), 2)

    def test_activity_import(self):
        """
        Les activités sont dépendantes des types d'ingrédients
        """
        test_path = f"{self.TEST_DIR_PATH}/element_models_creation/"
        call_command("load_ingredients", "2024-05-06", directory=test_path)

        self.assertTrue(all(obj.activity == IngredientActivity.ACTIVE for obj in Plant.objects.all()))
        self.assertTrue(all(obj.activity == IngredientActivity.ACTIVE for obj in Microorganism.objects.all()))
        self.assertTrue(all(obj.activity == IngredientActivity.ACTIVE for obj in Substance.objects.all()))

        self.assertTrue(
            all(
                obj.activity == IngredientActivity.ACTIVE
                for obj in Ingredient.objects.filter(ingredient_type=IngredientType.FORM_OF_SUPPLY)
            )
        )
        self.assertTrue(
            all(
                obj.activity == IngredientActivity.NOT_ACTIVE
                for obj in Ingredient.objects.filter(ingredient_type=IngredientType.AROMA)
            )
        )
        self.assertTrue(
            all(
                obj.activity == IngredientActivity.NOT_ACTIVE
                for obj in Ingredient.objects.filter(ingredient_type=IngredientType.ADDITIVE)
            )
        )
        self.assertTrue(
            all(
                obj.activity == IngredientActivity.NOT_ACTIVE
                for obj in Ingredient.objects.filter(ingredient_type=IngredientType.NON_ACTIVE_INGREDIENT)
            )
        )
        self.assertTrue(
            all(
                obj.activity == IngredientActivity.ACTIVE
                for obj in Ingredient.objects.filter(ingredient_type=IngredientType.ACTIVE_INGREDIENT)
            )
        )
