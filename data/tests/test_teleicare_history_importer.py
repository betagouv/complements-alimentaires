from unittest.mock import patch

from django.db import connection
from django.test import TestCase

from data.etl.teleicare_history.extractor import match_companies_on_siret_or_vat
from data.factories.company import CompanyFactory, _make_siret, _make_vat
from data.factories.teleicare_history import EtablissementFactory
from data.models.teleicare_history.etablissement import IcaEtablissement


class TeleicareHistoryImporterTestCase(TestCase):
    """
    Cette classe vise à tester les fonction liées à l'import d'historique de la plateforme TeleIcare
    """

    def setUp(self):
        """
        Adapted from: https://stackoverflow.com/a/49800437
        """
        super().setUp()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(IcaEtablissement)

            if IcaEtablissement._meta.db_table not in connection.introspection.table_names():
                raise ValueError(
                    "Table `{table_name}` is missing in test database.".format(
                        table_name=IcaEtablissement._meta.db_table
                    )
                )

    def tearDown(self):
        super().tearDown()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(IcaEtablissement)

    def test_match_companies_on_siret_or_vat(self):
        """
        Une entreprise enregistrée dans Teleicare ayant le même SIRET ou n° TVA intracom
        qu'une entreprise enregistrée dans Compl'Alim doit être liée par le siccrf_id
        """
        siret = _make_siret()
        etablissement_with_siret = EtablissementFactory(etab_siret=siret)
        company_with_siret = CompanyFactory(siret=siret)

        vat = _make_vat()
        etablissement_with_vat = EtablissementFactory(etab_siret=None, etab_numero_tva_intra=vat)
        company_with_vat = CompanyFactory(vat=vat)

        random_company = CompanyFactory()
        random_etablissement = EtablissementFactory()

        match_companies_on_siret_or_vat()
        company_with_siret.refresh_from_db()
        etablissement_with_siret.refresh_from_db()
        company_with_vat.refresh_from_db()
        etablissement_with_vat.refresh_from_db()
        random_company.refresh_from_db()
        random_etablissement.refresh_from_db()

        self.assertEqual(company_with_siret.siccrf_id, etablissement_with_siret.etab_ident)
        self.assertEqual(company_with_vat.siccrf_id, etablissement_with_vat.etab_ident)
        self.assertNotEqual(random_company.siccrf_id, random_etablissement.etab_ident)
        self.assertEqual(random_company.siccrf_id, None)

    @patch("data.etl.teleicare_history.extractor.logger")
    def test_match_companies_on_vat_used_twice(self, mocked_logger):
        """
        Si deux entreprises enregistrées dans Teleicare ont le même SIRET ou n° TVA intracom
        alors le matching avec une Company Compl'Alim avec la contrainte d'unicité sur ces deux champs
        n'est pas évident
        """
        vat_used_twice = _make_vat()
        _ = EtablissementFactory(etab_siret=None, etab_numero_tva_intra=vat_used_twice)
        _ = EtablissementFactory(etab_siret=None, etab_numero_tva_intra=vat_used_twice)
        _ = CompanyFactory(vat=vat_used_twice)

        match_companies_on_siret_or_vat()
        mocked_logger.error.assert_called_with(
            "Plusieurs Etablissement provenant de Teleicare ont le même n° TVA, ce qui rend le matching avec une Company Compl'Alim incertain."
        )
