from django.test import TestCase
from unittest.mock import patch

from django.core.management import call_command
from django.db.models import TextField, CharField, FloatField, IntegerField

from data.csv_importer import import_csv, _clean_value
from data.models import Plant, PlantFamily, PlantPart, Ingredient, Microorganism, Substance


class CSVImporterTestCase(TestCase):
    @patch("data.csv_importer.logger")
    def test_unknown_file_is_not_imported(self, mocked_logger):
        file_name = "déclaration_impots_2002.csv"
        import_csv(file_name)
        mocked_logger.error.assert_called_with(
            "Ce nom de fichier ne ressemble pas à ceux attendus : 'déclaration_impots_2002.csv'"
        )

    @patch("data.csv_importer.logger")
    def test_non_csv_file_is_not_imported(self, mocked_logger):
        file_name = "REF_ICA_INGREDIENT_AUTRE.pdf"
        import_csv(file_name)
        mocked_logger.error.assert_called_with("'REF_ICA_INGREDIENT_AUTRE.pdf' n'est pas un fichier csv.")

    def test_clean_values(self):
        """TextField should be "" if no value istead of "NULL"
        FloatField should work with french decimal values with a comma
        """
        self.assertEqual(2.5, _clean_value("2,5", FloatField()))
        self.assertEqual(2.5, _clean_value("2.5", FloatField()))
        self.assertEqual("2,5", _clean_value("2,5", IntegerField()))
        self.assertEqual(None, _clean_value("NULL", IntegerField()))
        self.assertEqual(None, _clean_value("", FloatField()))
        self.assertEqual(None, _clean_value("", IntegerField()))
        self.assertEqual("", _clean_value("", TextField()))
        self.assertEqual("", _clean_value("NULL", TextField()))
        self.assertEqual("", _clean_value("NULL", CharField()))
        self.assertEqual("Eloides rhamnosus trulul", _clean_value(" Eloides rhamnosus trulul ", CharField()))

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

        self.assertEqual(len(Plant.objects.get(name="Pour les pieds").useful_parts.all()), 1)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").useful_parts.all()), 3)

    def test_create_objects_in_relation_if_they_do_not_already_exist(self):
        path = "data/tests/files/create_objects_in_relation_if_they_do_not_already_exist/"
        call_command("load_ingredients", directory=path)

        self.assertEqual(len(Plant.objects.get(name="Pour les pieds").useful_parts.all()), 1)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").useful_parts.all()), 4)
        self.assertEqual(len(Plant.objects.get(name="Pour le cou").useful_parts.all()), 4)
        first_id = Plant.objects.get(siccrf_id=1)
        self.assertEqual(len(first_id.useful_parts.all()), 1)
        self.assertEqual(first_id.name, "1")
        second_id = Plant.objects.get(siccrf_id=2)
        # dans le fichier une ligne de relation est dupliquée
        self.assertEqual(len(second_id.useful_parts.all()), 2)
        self.assertEqual(second_id.name, "2")

    @patch("data.csv_importer.logger")
    def test_raises_if_not_utf_8_file(self, mocked_logger):
        path = "data/tests/files/raises_if_not_utf_8_file/"
        call_command("load_ingredients", directory=path)
        mocked_logger.error.assert_called_with("'REF_ICA_PLANTE.csv' n'est pas un fichier unicode.")

    def test_missing_import_data_field_well_filled(self):
        path = "data/tests/files/create_objects_in_relation_if_they_do_not_already_exist/"
        call_command("load_ingredients", directory=path)

        missing_plants = Plant.objects.filter(missing_import_data=True)
        missing_plantparts = PlantPart.objects.filter(missing_import_data=True)
        self.assertEqual(len(missing_plants), 2)
        for plant in missing_plants:
            self.assertIn(plant.name, ["2", "1"])
            self.assertEqual(plant.public_comments, "")
            self.assertEqual(plant.private_comments, "")
            self.assertEqual(plant.is_obsolete, False)
            self.assertEqual(plant.family, None)
            self.assertFalse(plant.substances.all().exists())
            self.assertTrue(plant.useful_parts.all().exists())

        self.assertEqual(len(missing_plantparts), 1)
        self.assertEqual(missing_plantparts[0].name, "40")
        for plantparts in missing_plantparts:
            self.assertEqual(plantparts.name_en, "")
            self.assertEqual(plantparts.is_obsolete, False)
            self.assertTrue(plantparts.usefulpart_set.all().exists())
            self.assertTrue(plantparts.plant_set.all().exists())
