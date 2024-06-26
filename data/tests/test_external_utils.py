from django.test import TestCase

from data.utils.external_utils import SiretData


class SiretDataTestCase(TestCase):
    def test_get_formatted_company_data(self):
        # https://api.insee.fr/entreprises/sirene/V3.11/siret/82073111500037
        raw_siret_data = {
            "header": {"statut": 200, "message": "ok"},
            "etablissement": {
                "siren": "820731115",
                "nic": "00037",
                "siret": "82073111500037",
                "statutDiffusionEtablissement": "O",
                "dateCreationEtablissement": "2020-02-28",
                "trancheEffectifsEtablissement": "22",
                "anneeEffectifsEtablissement": "2021",
                "activitePrincipaleRegistreMetiersEtablissement": None,
                "dateDernierTraitementEtablissement": "2024-03-30T02:59:09.849",
                "etablissementSiege": True,
                "nombrePeriodesEtablissement": 1,
                "uniteLegale": {
                    "etatAdministratifUniteLegale": "A",
                    "statutDiffusionUniteLegale": "O",
                    "dateCreationUniteLegale": "2016-05-27",
                    "categorieJuridiqueUniteLegale": "5710",
                    "denominationUniteLegale": "TOO GOOD TO GO FRANCE",
                    "sigleUniteLegale": None,
                    "denominationUsuelle1UniteLegale": None,
                    "denominationUsuelle2UniteLegale": None,
                    "denominationUsuelle3UniteLegale": None,
                    "sexeUniteLegale": None,
                    "nomUniteLegale": None,
                    "nomUsageUniteLegale": None,
                    "prenom1UniteLegale": None,
                    "prenom2UniteLegale": None,
                    "prenom3UniteLegale": None,
                    "prenom4UniteLegale": None,
                    "prenomUsuelUniteLegale": None,
                    "pseudonymeUniteLegale": None,
                    "activitePrincipaleUniteLegale": "82.99Z",
                    "nomenclatureActivitePrincipaleUniteLegale": "NAFRev2",
                    "identifiantAssociationUniteLegale": None,
                    "economieSocialeSolidaireUniteLegale": "N",
                    "societeMissionUniteLegale": None,
                    "caractereEmployeurUniteLegale": None,
                    "trancheEffectifsUniteLegale": "22",
                    "anneeEffectifsUniteLegale": "2021",
                    "nicSiegeUniteLegale": "00037",
                    "dateDernierTraitementUniteLegale": "2024-03-22T09:28:19.000",
                    "categorieEntreprise": "PME",
                    "anneeCategorieEntreprise": "2021",
                },
                "adresseEtablissement": {
                    "complementAdresseEtablissement": None,
                    "numeroVoieEtablissement": "12",
                    "indiceRepetitionEtablissement": None,
                    "dernierNumeroVoieEtablissement": None,
                    "indiceRepetitionDernierNumeroVoieEtablissement": None,
                    "typeVoieEtablissement": "RUE",
                    "libelleVoieEtablissement": "DUHESME",
                    "codePostalEtablissement": "75018",
                    "libelleCommuneEtablissement": "PARIS",
                    "libelleCommuneEtrangerEtablissement": None,
                    "distributionSpecialeEtablissement": None,
                    "codeCommuneEtablissement": "75118",
                    "codeCedexEtablissement": None,
                    "libelleCedexEtablissement": None,
                    "codePaysEtrangerEtablissement": None,
                    "libellePaysEtrangerEtablissement": None,
                    "identifiantAdresseEtablissement": "751182974_B",
                    "coordonneeLambertAbscisseEtablissement": "48.890627",
                    "coordonneeLambertOrdonneeEtablissement": "2.338061",
                },
                "adresse2Etablissement": {
                    "complementAdresse2Etablissement": None,
                    "numeroVoie2Etablissement": None,
                    "indiceRepetition2Etablissement": None,
                    "typeVoie2Etablissement": None,
                    "libelleVoie2Etablissement": None,
                    "codePostal2Etablissement": None,
                    "libelleCommune2Etablissement": None,
                    "libelleCommuneEtranger2Etablissement": None,
                    "distributionSpeciale2Etablissement": None,
                    "codeCommune2Etablissement": None,
                    "codeCedex2Etablissement": None,
                    "libelleCedex2Etablissement": None,
                    "codePaysEtranger2Etablissement": None,
                    "libellePaysEtranger2Etablissement": None,
                },
                "periodesEtablissement": [
                    {
                        "dateFin": None,
                        "dateDebut": "2020-02-28",
                        "etatAdministratifEtablissement": "A",
                        "changementEtatAdministratifEtablissement": False,
                        "enseigne1Etablissement": None,
                        "enseigne2Etablissement": None,
                        "enseigne3Etablissement": None,
                        "changementEnseigneEtablissement": False,
                        "denominationUsuelleEtablissement": None,
                        "changementDenominationUsuelleEtablissement": False,
                        "activitePrincipaleEtablissement": "82.99Z",
                        "nomenclatureActivitePrincipaleEtablissement": "NAFRev2",
                        "changementActivitePrincipaleEtablissement": False,
                        "caractereEmployeurEtablissement": "N",
                        "changementCaractereEmployeurEtablissement": False,
                    }
                ],
            },
        }

        expected_result = {
            "social_name": "TOO GOOD TO GO FRANCE",
            "address": "12 RUE DUHESME",
            "city": "PARIS",
            "postal_code": "75018",
            "cedex": "",
        }

        self.assertEqual(SiretData.get_formatted_company_data(raw_siret_data), expected_result)
