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
        path = "data/tests/files/test-model-creation-1/"
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

    def test_linked_models_created(self):
        path = "data/tests/files/test-model-creation-1/"
        call_command("load_ingredients", directory=path)
        self.assertTrue(PlantFamily.objects.filter(siccrf_id=6).exists())
