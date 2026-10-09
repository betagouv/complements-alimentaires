from django.test import TestCase

from data.utils.external_utils import SiretData


class SiretDataTestCase(TestCase):
    def test_get_formatted_company_data(self):
        # https://recherche-entreprises.api.gouv.fr/search?q=82073111500037
        raw_siret_data = {
            "header": {"statut": 200, "message": "ok"},
            "results": [
                {
                    "siren": "820731115",
                    "nom_raison_sociale": "TOO GOOD TO GO FRANCE",
                    "date_fermature": None,
                    "siege": {
                        "numero_voie": "12",
                        "type_voie": "RUE",
                        "libelle_voie": "DUHESME",
                        "complement_adresse": None,
                        "dernier_numero_voie": None,
                        "indice_repetition": None,
                        "code_postal": "75018",
                        "libelle_commune": "PARIS",
                        "cedex": None,
                        "libelle_cedex": None,
                        "nom_commercial": None,
                    },
                }
            ],
            "total_results": 1,
        }

        expected_result = {
            "social_name": "TOO GOOD TO GO FRANCE",
            "commercial_name": None,
            "address": "12 RUE DUHESME",
            "city": "PARIS",
            "postal_code": "75018",
            "cedex": "",
        }

        self.assertEqual(SiretData.get_formatted_company_data(raw_siret_data), expected_result)

        # TODO: handle case where no results are returned (and too many?)
        # TODO: handle foreign addresses?
        # TODO: handle [NON-DIFFUSABLE] particularly in concatenated strings
