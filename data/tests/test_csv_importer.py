from django.test import TestCase
from unittest.mock import patch

from django.core.management import call_command
from django.db.models import TextField, CharField, FloatField, IntegerField

from data.csv_importer import import_csv_from_filepath, CSVImporter
from data.utils.importer_utils import clean_value
from data.exceptions import CSVFileError
from data.models import Plant, PlantFamily, PlantPart, Ingredient, Microorganism, Substance


class CSVImporterTestCase(TestCase):
    def test_unknown_file_is_not_imported(self):
        file_name = "déclaration_impots_2002.csv"

        with self.assertRaises(CSVFileError) as context:
            import_csv_from_filepath(file_name)
        self.assertEqual(
            "Ce nom de fichier ne ressemble pas à ceux attendus : 'déclaration_impots_2002.csv'",
            context.exception.message,
        )

    def test_non_csv_file_is_not_imported(self):
        with open("data/tests/files/raises_if_not_csv/blank.pdf") as file:
            with self.assertRaises(CSVFileError) as context:
                CSVImporter(file, Plant)
            self.assertEqual("'blank.pdf' n'est pas un fichier csv.", context.exception.message)

    @patch("data.management.commands.load_ingredients.logger")
    def test_raises_if_not_utf_8_file(self, mocked_logger):
        path = "data/tests/files/raises_if_not_utf_8_file/"
        call_command("load_ingredients", directory=path)

        mocked_logger.error.assert_called_with("'REF_ICA_PLANTE.csv' n'est pas un fichier unicode.")

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

    def test_models_created(self):
        path = "data/tests/files/test_model_creation/"
        call_command("load_ingredients", directory=path)

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

    def test_linked_models_created_even_if_no_corresponding_file(self):
        path = "data/tests/files/test_model_creation/"
        call_command("load_ingredients", directory=path)
        self.assertTrue(PlantFamily.objects.filter(siccrf_id=6).exists())
        self.assertEqual(PlantFamily.objects.get(siccrf_id=6).missing_import_data, True)
        self.assertEqual(PlantFamily.objects.get(siccrf_id=6).name, "")

    def test_import_twice_same_synonym_created_only_once(self):
        path = "data/tests/files/import_twice_same_synonym_created_only_once/"
        call_command("load_ingredients", directory=path)
        # les lignes doublonnées ne sont pas ajoutées
        self.assertEqual(len(Plant.objects.get(name="Pour les pieds").plantsynonym_set.all()), 4)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").plantsynonym_set.all()), 3)
        # mais les lignes dont l'id est différent sont ajoutées 2 fois
        self.assertEqual(
            len(Plant.objects.get(name="Pour les pieds").plantsynonym_set.filter(name="Chaussure à talons")), 2
        )

    def test_creates_models_with_their_relations(self):
        path = "data/tests/files/creates_models_with_their_relations/"
        call_command("load_ingredients", directory=path)

        self.assertEqual(len(Plant.objects.get(name="Pour les pieds").plant_parts.all()), 1)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").plant_parts.all()), 3)

    def test_create_objects_in_relation_if_they_do_not_already_exist(self):
        path = "data/tests/files/create_objects_in_relation_if_they_do_not_already_exist/"
        call_command("load_ingredients", directory=path)

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

    def test_missing_import_data_field_well_filled(self):
        path = "data/tests/files/create_objects_in_relation_if_they_do_not_already_exist/"
        call_command("load_ingredients", directory=path)

        missing_plants = Plant.objects.filter(missing_import_data=True)
        missing_plantparts = PlantPart.objects.filter(missing_import_data=True)
        self.assertEqual(len(missing_plants), 2)
        for plant in missing_plants:
            self.assertIn(plant.name, ["", ""])
            self.assertEqual(plant.public_comments, "")
            self.assertEqual(plant.private_comments, "")
            self.assertEqual(plant.is_obsolete, False)
            self.assertEqual(plant.family, None)
            self.assertFalse(plant.substances.all().exists())
            self.assertTrue(plant.plant_parts.all().exists())

        self.assertEqual(len(missing_plantparts), 1)
        self.assertEqual(missing_plantparts[0].name, "")
        for plantparts in missing_plantparts:
            self.assertEqual(plantparts.name_en, "")
            self.assertEqual(plantparts.is_obsolete, False)
            self.assertTrue(plantparts.part_set.all().exists())
            self.assertTrue(plantparts.plant_set.all().exists())

    def test_plantparts_status_is_not_always_useful(self):
        """
        Il existe des plantparts avec siccrf_is_useful = False et siccrf_must_be_monitored = True
        """
        path = "data/tests/files/create_plants_with_distinct_useful_and_to_be_monitored_parts/"
        call_command("load_ingredients", directory=path)

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
