from django.test import TestCase

from data.utils.external_utils import SiretData


class SiretDataTestCase(TestCase):
    def test_get_formatted_company_data(self):
        # https://recherche-entreprises.api.gouv.fr/search?q=...
        raw_siret_data = {
            "header": {"statut": 200, "message": "ok"},
            "results": [
                {
                    "nom_raison_sociale": "COMPANY NAME SL",
                    "date_fermeture": "2020-01-01",
                    "siege": {
                        "numero_voie": "12",
                        "type_voie": "RUE",
                        "libelle_voie": "ABEILLES",
                        "complement_adresse": "Étage 3",
                        "dernier_numero_voie": "1",
                        "indice_repetition": "B",
                        "code_postal": "75001",
                        "libelle_commune": "PARIS",
                        "cedex": "75000",
                        "libelle_cedex": "PARIS CEDEX",
                        "nom_commercial": "Company name",
                    },
                }
            ],
            "total_results": 1,
        }

        expected_result = {
            "status": 200,
            "social_name": "COMPANY NAME SL",
            "commercial_name": "Company name",
            "address": "12 B 1 RUE ABEILLES",
            "additional_details": "Étage 3",
            "city": "PARIS",
            "postal_code": "75001",
            "cedex": "75000 PARIS CEDEX",
            "end_date": "2020-01-01",
        }

        self.assertEqual(SiretData.get_formatted_company_data(raw_siret_data), expected_result)

    def test_no_results(self):
        raw_siret_data = {
            "header": {"statut": 200, "message": "ok"},
            "results": [],
            "total_results": 0,
        }

        expected_result = {"status": 404}

        self.assertEqual(SiretData.get_formatted_company_data(raw_siret_data), expected_result)
        # TODO: handle case where multiple results returned?
        # TODO: handle foreign addresses?
        # TODO: handle [NON-DIFFUSABLE] particularly in concatenated strings

    def test_unexpected_missing_keys(self):
        raw_siret_data = {
            "header": {"statut": 200, "message": "ok"},
            "results": [{"surprise": "the data you expected is missing"}],
            "total_results": 0,
        }

        expected_result = {"status": 500}

        self.assertEqual(SiretData.get_formatted_company_data(raw_siret_data), expected_result)
