from django.test import TestCase
from unittest.mock import patch

from django.db.models import TextField, CharField, FloatField, IntegerField

from data.csv_importer import import_csv, _clean_value


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
        self.assertEqual(None, _clean_value(None, IntegerField()))
        self.assertEqual("", _clean_value("NULL", TextField()))
        self.assertEqual("", _clean_value("NULL", CharField()))
