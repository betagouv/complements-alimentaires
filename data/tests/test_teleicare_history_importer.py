import datetime
from unittest.mock import patch

from django.db import connection
from django.test import TestCase

from data.etl.teleicare_history.extractor import (
    create_declarations_from_teleicare_history,
    match_companies_on_siret_or_vat,
)
from data.factories.company import CompanyFactory, EtablissementToCompanyRelationFactory, _make_siret, _make_vat
from data.factories.declaration import AuthorizedDeclarationFactory
from data.factories.galenic_formulation import GalenicFormulationFactory
from data.factories.population import PopulationFactory
from data.factories.teleicare_history import (
    ComplementAlimentaireFactory,
    DeclarationFactory,
    EtablissementFactory,
    IcaPopulationCibleDeclareeFactory,
    VersionDeclarationFactory,
)
from data.factories.unit import SubstanceUnitFactory
from data.models.company import EtablissementToCompanyRelation
from data.models.declaration import Declaration
from data.models.teleicare_history.ica_declaration import (
    IcaComplementAlimentaire,
    IcaDeclaration,
    IcaEffetDeclare,
    IcaPopulationCibleDeclaree,
    IcaPopulationRisqueDeclaree,
    IcaVersionDeclaration,
)
from data.models.teleicare_history.ica_etablissement import IcaEtablissement


class TeleicareHistoryImporterTestCase(TestCase):
    """
    Cette classe vise à tester les fonction liées à l'import d'historique de la plateforme TeleIcare
    """

    def setUp(self):
        """
        Adapted from: https://stackoverflow.com/a/49800437
        """
        super().setUp()
        self.galenic_formulation_id = 1
        self.galenic_formulation = GalenicFormulationFactory(siccrf_id=self.galenic_formulation_id)
        self.unit_id = 1
        self.unit = SubstanceUnitFactory(siccrf_id=self.unit_id)
        for table in [
            IcaEtablissement,
            IcaComplementAlimentaire,
            IcaDeclaration,
            IcaVersionDeclaration,
            IcaEffetDeclare,
            IcaPopulationCibleDeclaree,
            IcaPopulationRisqueDeclaree,
        ]:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(table)

                if table._meta.db_table not in connection.introspection.table_names():
                    raise ValueError(
                        "Table `{table_name}` is missing in test database.".format(table_name=table._meta.db_table)
                    )

    def tearDown(self):
        super().tearDown()
        for table in [IcaVersionDeclaration, IcaComplementAlimentaire, IcaDeclaration, IcaEtablissement]:
            table.objects.all().delete()
            # la suppression des modèles fail avec l'erreur
            # django.db.utils.OperationalError: cannot DROP TABLE "ica_versiondeclaration" because it has pending trigger events
            # même avec un sleep(15)
            # with connection.schema_editor() as schema_editor:
            # schema_editor.delete_model(table)

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
        random_etablissement = EtablissementFactory(
            etab_ica_fabricant=True,
        )

        match_companies_on_siret_or_vat(create_only_useful=False)
        company_with_siret.refresh_from_db()
        etablissement_with_siret.refresh_from_db()
        company_with_vat.refresh_from_db()
        etablissement_with_vat.refresh_from_db()
        random_company.refresh_from_db()
        random_etablissement.refresh_from_db()

        self.assertTrue(
            EtablissementToCompanyRelation.objects.filter(
                siccrf_id=etablissement_with_siret.etab_ident, company=company_with_siret
            ).exists()
        )
        self.assertTrue(
            EtablissementToCompanyRelation.objects.filter(
                siccrf_id=etablissement_with_vat.etab_ident, company=company_with_vat
            ).exists()
        )
        self.assertFalse(
            EtablissementToCompanyRelation.objects.filter(
                siccrf_id=random_etablissement.etab_ident, company=random_company
            ).exists()
        )
        self.assertFalse(EtablissementToCompanyRelation.objects.filter(company=random_company).exists())

    def test_match_companies_on_vat_used_twice(self):
        """
        Une entreprise Compl'Alim peut être en lien avec plus d'un Etablissement Teleicare
        Soit via son vat/siret actuel, soit via un old_siret/vat ajouté à la table EtablissementToCompanyRelation
        Si c'est via son vat/siret actuel, une entrée à EtablissementToCompanyRelation est créée
        """
        vat_1 = _make_vat()
        etab_1 = EtablissementFactory(etab_siret=None, etab_numero_tva_intra=vat_1)
        vat_2 = _make_vat()
        etab_2 = EtablissementFactory(etab_siret=None, etab_numero_tva_intra=vat_2)
        company = CompanyFactory(vat=vat_2)
        EtablissementToCompanyRelationFactory(company=company, old_vat=vat_1)

        self.assertEqual(
            EtablissementToCompanyRelation.objects.filter(company=company).count(),
            1,
        )
        self.assertFalse(
            EtablissementToCompanyRelation.objects.filter(company=company, old_vat=vat_2).exists(),
        )

        match_companies_on_siret_or_vat(create_only_useful=False)
        self.assertEqual(
            EtablissementToCompanyRelation.objects.filter(company=company).count(),
            2,
        )
        self.assertTrue(
            EtablissementToCompanyRelation.objects.filter(company=company, old_vat=vat_2).exists(),
        )  # cette relation a été créée lors du matching
        self.assertListEqual(
            list(EtablissementToCompanyRelation.objects.filter(company=company).values_list("siccrf_id", flat=True)),
            [etab_1.etab_ident, etab_2.etab_ident],
        )

    def test_create_new_companies(self):
        """
        Si une entreprise enregistrée dans TeleIcare n'existe pas encore dans Compl'Alim, elle est créée
        """

        etablissement_to_create_as_company = EtablissementFactory(etab_siret=None, etab_ica_importateur=True)
        # devrait être créée malgré le numéro de téléphone mal formaté
        EtablissementFactory(etab_siret=None, etab_ica_importateur=True, etab_telephone="0345")
        self.assertEqual(
            EtablissementToCompanyRelation.objects.filter(
                siccrf_id=etablissement_to_create_as_company.etab_ident
            ).count(),
            0,
        )

        match_companies_on_siret_or_vat(create_if_not_exist=True, create_only_useful=False)
        self.assertTrue(
            EtablissementToCompanyRelation.objects.filter(
                siccrf_id=etablissement_to_create_as_company.etab_ident
            ).exists()
        )
        self.assertEqual(
            EtablissementToCompanyRelation.objects.exclude(siccrf_id=None).count(),
            2,
            "Le champ siccrf_id n'a pas été rempli lors du matching",
        )

        created_relation = EtablissementToCompanyRelation.objects.get(
            siccrf_id=etablissement_to_create_as_company.etab_ident
        )
        self.assertEqual(created_relation.siccrf_id, etablissement_to_create_as_company.etab_ident)
        self.assertEqual(created_relation.company.address, etablissement_to_create_as_company.etab_adre_voie)
        self.assertEqual(created_relation.company.postal_code, etablissement_to_create_as_company.etab_adre_cp)
        self.assertEqual(created_relation.company.city, etablissement_to_create_as_company.etab_adre_ville)

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    @patch("data.etl.teleicare_history.extractor.add_product_info_from_teleicare_history")
    def test_create_declarations_from_history(self, mocked_add_composition_function, mocked_add_product_function):
        """
        Les déclarations sont créées à partir d'object historiques des modèles Ica_
        """

        etablissement_to_create_as_company = EtablissementFactory(etab_siret=None, etab_ica_importateur=True)

        CA_to_create_as_declaration = ComplementAlimentaireFactory(
            etab=etablissement_to_create_as_company, frmgal_ident=self.galenic_formulation_id
        )
        declaration_to_create_as_declaration = DeclarationFactory(
            cplalim=CA_to_create_as_declaration, tydcl_ident=1, etab=None
        )
        version_declaration_to_create_as_declaration = VersionDeclarationFactory(
            dcl=declaration_to_create_as_declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )

        match_companies_on_siret_or_vat(create_if_not_exist=True)
        create_declarations_from_teleicare_history()

        version_declaration_to_create_as_declaration.refresh_from_db()
        created_declaration = Declaration.objects.get(siccrf_id=CA_to_create_as_declaration.cplalim_ident)
        self.assertEqual(
            created_declaration.company,
            EtablissementToCompanyRelation.objects.get(
                siccrf_id=etablissement_to_create_as_company.etab_ident
            ).company,
        )
        self.assertIsNone(created_declaration.mandated_company)
        self.assertEqual(created_declaration.name, CA_to_create_as_declaration.cplalim_nom)
        self.assertEqual(created_declaration.brand, CA_to_create_as_declaration.cplalim_marque)
        self.assertEqual(created_declaration.gamme, CA_to_create_as_declaration.cplalim_gamme)
        self.assertEqual(created_declaration.flavor, CA_to_create_as_declaration.dclencours_gout_arome_parfum)
        self.assertEqual(created_declaration.galenic_formulation, self.galenic_formulation)
        self.assertEqual(created_declaration.daily_recommended_dose, "32 kg of ppo")
        self.assertEqual(created_declaration.unit_measurement, self.unit)
        self.assertEqual(created_declaration.article, Declaration.Article.ARTICLE_15)
        self.assertEqual(
            created_declaration.conditioning, version_declaration_to_create_as_declaration.vrsdecl_conditionnement
        )
        self.assertEqual(
            created_declaration.unit_quantity, version_declaration_to_create_as_declaration.vrsdecl_poids_uc
        )
        self.assertEqual(
            created_declaration.minimum_duration,
            str(version_declaration_to_create_as_declaration.vrsdecl_durabilite),
        )

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    @patch("data.etl.teleicare_history.extractor.add_product_info_from_teleicare_history")
    def test_create_declarations_from_history_for_specific_company(
        self, mocked_add_composition_function, mocked_add_product_function
    ):
        """
        Les déclarations sont créées à partir d'object historiques des modèles Ica_ seulement pour les companies spécifiées
        """
        etablissement_to_create_as_company = EtablissementFactory(etab_siret=None, etab_ica_importateur=True)
        matching_company = CompanyFactory()
        EtablissementToCompanyRelationFactory(
            company=matching_company, siccrf_id=etablissement_to_create_as_company.etab_ident
        )

        CA_to_create_as_declaration = ComplementAlimentaireFactory(
            etab=etablissement_to_create_as_company, frmgal_ident=self.galenic_formulation_id
        )
        declaration_to_create_as_declaration = DeclarationFactory(cplalim=CA_to_create_as_declaration, tydcl_ident=1)
        version_declaration_to_create_as_declaration = VersionDeclarationFactory(
            dcl=declaration_to_create_as_declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        other_etablissement = EtablissementFactory(etab_siret=None, etab_ica_importateur=True)
        other_company = CompanyFactory()
        EtablissementToCompanyRelationFactory(company=other_company, siccrf_id=other_etablissement.etab_ident)
        other_CA = ComplementAlimentaireFactory(etab=other_etablissement)
        other_declaration = DeclarationFactory(cplalim=other_CA, tydcl_ident=1)
        VersionDeclarationFactory(
            dcl=other_declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            vrsdecl_djr="32 kg of ppo",
        )

        create_declarations_from_teleicare_history(company_ids=[matching_company.id])

        version_declaration_to_create_as_declaration.refresh_from_db()
        self.assertEqual(Declaration.objects.all().count(), 1)
        self.assertEqual(Declaration.objects.all()[0].name, CA_to_create_as_declaration.cplalim_nom)
        self.assertEqual(Declaration.objects.all()[0].siccrf_id, CA_to_create_as_declaration.cplalim_ident)
        self.assertEqual(Declaration.objects.filter(siccrf_id=other_CA.cplalim_ident).exists(), False)

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    @patch("data.etl.teleicare_history.extractor.add_product_info_from_teleicare_history")
    def test_acceptation_snapshot_is_created(self, mocked_add_composition_function, mocked_add_product_function):
        etablissement = EtablissementFactory(etab_siret=None, etab_ica_importateur=True)
        CA = ComplementAlimentaireFactory(etab=etablissement, frmgal_ident=self.galenic_formulation_id)
        oldest_declaration = DeclarationFactory(
            cplalim=CA,
            tydcl_ident=1,
            dcl_date="06/20/2017 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        latest_declaration = DeclarationFactory(
            cplalim=CA,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        VersionDeclarationFactory(
            dcl=oldest_declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        VersionDeclarationFactory(
            dcl=latest_declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        match_companies_on_siret_or_vat(create_if_not_exist=True)
        create_declarations_from_teleicare_history()
        declaration = Declaration.objects.get(siccrf_id=CA.cplalim_ident)
        self.assertEqual(
            declaration.creation_date, datetime.datetime(2017, 6, 20, 20, 20, 20, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(
            declaration.modification_date, datetime.datetime(2021, 3, 20, 20, 20, 20, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(
            declaration.snapshots.all().count(),
            1,
        )
        self.assertEqual(
            declaration.acceptation_date,
            datetime.datetime(2021, 3, 20, 20, 20, 20, tzinfo=datetime.timezone.utc),
        )
        self.assertEqual(
            declaration.snapshots.all().first().creation_date,
            datetime.datetime(2021, 3, 20, 20, 20, 20, tzinfo=datetime.timezone.utc),
        )

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    @patch("data.etl.teleicare_history.extractor.add_product_info_from_teleicare_history")
    def test_declaration_is_created_even_if_latest_ica_declaration_has_no_version_declaration(
        self, mocked_add_composition_function, mocked_add_product_function
    ):
        etablissement = EtablissementFactory(etab_siret=None, etab_ica_importateur=True)

        CA = ComplementAlimentaireFactory(etab=etablissement, frmgal_ident=self.galenic_formulation_id)
        oldest_declaration_to_create_as_declaration = DeclarationFactory(
            cplalim=CA,
            tydcl_ident=1,
            dcl_date="06/20/2017 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        DeclarationFactory(
            cplalim=CA,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        version_declaration_to_create_as_declaration = VersionDeclarationFactory(
            dcl=oldest_declaration_to_create_as_declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        match_companies_on_siret_or_vat(create_if_not_exist=True)
        create_declarations_from_teleicare_history()
        declaration = Declaration.objects.filter(siccrf_id=CA.cplalim_ident)
        self.assertTrue(declaration.exists())
        self.assertEqual(declaration.count(), 1)
        self.assertEqual(
            declaration[0].creation_date, datetime.datetime(2017, 6, 20, 20, 20, 20, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(
            declaration[0].modification_date, datetime.datetime(2017, 6, 20, 20, 20, 20, tzinfo=datetime.timezone.utc)
        )
        self.assertEqual(
            declaration[0].galenic_formulation,
            self.galenic_formulation,
        )
        self.assertEqual(
            declaration[0].unit_measurement,
            self.unit,
        )
        self.assertEqual(
            declaration[0].daily_recommended_dose,
            version_declaration_to_create_as_declaration.vrsdecl_djr,
        )

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    def test_historic_declaration_has_right_populations(self, mocked_add_composition_function):
        PopulationFactory(id=8, name="Femme enceinte")
        PopulationFactory(id=9, name="Femme allaitante")

        siret = _make_siret()
        etablissement = EtablissementFactory(etab_siret=siret)
        company = CompanyFactory(siret=siret)
        EtablissementToCompanyRelationFactory(company=company, old_siret=siret)
        CA_1 = ComplementAlimentaireFactory(etab=etablissement, frmgal_ident=self.galenic_formulation_id)
        declaration_1 = DeclarationFactory(
            cplalim=CA_1,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        version_declaration_1 = VersionDeclarationFactory(
            dcl=declaration_1,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        CA_2 = ComplementAlimentaireFactory(etab=etablissement, frmgal_ident=self.galenic_formulation_id)
        declaration_2 = DeclarationFactory(
            cplalim=CA_2,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        version_declaration_2 = VersionDeclarationFactory(
            dcl=declaration_2,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        CA_3 = ComplementAlimentaireFactory(etab=etablissement, frmgal_ident=self.galenic_formulation_id)
        declaration_3 = DeclarationFactory(
            cplalim=CA_3,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        version_declaration_3 = VersionDeclarationFactory(
            dcl=declaration_3,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        IcaPopulationCibleDeclareeFactory(
            vrsdecl_ident=version_declaration_1.vrsdecl_ident, popcbl_ident=11
        )  # Femme allaitante
        IcaPopulationCibleDeclareeFactory(
            vrsdecl_ident=version_declaration_2.vrsdecl_ident, popcbl_ident=10
        )  # Femme enceinte
        IcaPopulationCibleDeclareeFactory(vrsdecl_ident=version_declaration_3.vrsdecl_ident, popcbl_ident=2)  # Autre
        match_companies_on_siret_or_vat()
        create_declarations_from_teleicare_history()
        CA_dec_1 = Declaration.objects.get(siccrf_id=CA_1.cplalim_ident)
        self.assertIn("Femme allaitante", CA_dec_1.populations.all().values_list("name", flat=True))
        CA_dec_2 = Declaration.objects.get(siccrf_id=CA_2.cplalim_ident)
        self.assertIn("Femme enceinte", CA_dec_2.populations.all().values_list("name", flat=True))
        CA_dec_3 = Declaration.objects.get(siccrf_id=CA_3.cplalim_ident)
        self.assertFalse(CA_dec_3.populations.all().exists())

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    def test_historic_declaration_has_right_mandated_company_with_all_historic_companies_created(
        self, mocked_add_composition_function
    ):
        siret_declarant = _make_siret()
        siret_mandataire = _make_siret()
        etablissement_declarant = EtablissementFactory(etab_siret=siret_declarant)
        etablissement_mandataire = EtablissementFactory(etab_siret=siret_mandataire)
        CA = ComplementAlimentaireFactory(etab=etablissement_declarant, frmgal_ident=self.galenic_formulation_id)
        declaration = DeclarationFactory(
            cplalim=CA,
            etab=etablissement_mandataire,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        version_declaration = VersionDeclarationFactory(
            dcl=declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        match_companies_on_siret_or_vat(create_if_not_exist=True)
        create_declarations_from_teleicare_history()
        CA_declaration = Declaration.objects.get(siccrf_id=CA.cplalim_ident)
        declarant_company = EtablissementToCompanyRelation.objects.get(
            siccrf_id=etablissement_declarant.etab_ident
        ).company
        mandataire_company = EtablissementToCompanyRelation.objects.get(
            siccrf_id=etablissement_mandataire.etab_ident
        ).company  # les objets Company et EtablissementToCompanyRelation ont été créés
        self.assertEqual(CA_declaration.mandated_company, mandataire_company)
        self.assertEqual(CA_declaration.company, declarant_company)
        self.assertEqual(CA_declaration.address, version_declaration.vrsdecl_adre_voie)
        self.assertEqual(CA_declaration.postal_code, version_declaration.vrsdecl_adre_cp[:10])
        self.assertEqual(CA_declaration.city, version_declaration.vrsdecl_adre_ville)

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    def test_historic_declaration_has_right_mandated_company_without_precreation_mandated_companies(
        self, mocked_add_composition_function
    ):
        siret_declarant = _make_siret()
        siret_mandataire = _make_siret()
        etablissement_declarant = EtablissementFactory(etab_siret=siret_declarant)
        declarant_company = CompanyFactory(siret=siret_declarant)

        etablissement_mandataire = EtablissementFactory(etab_siret=siret_mandataire)
        CA = ComplementAlimentaireFactory(etab=etablissement_declarant, frmgal_ident=self.galenic_formulation_id)
        declaration = DeclarationFactory(
            cplalim=CA,
            etab=etablissement_mandataire,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        VersionDeclarationFactory(
            dcl=declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        match_companies_on_siret_or_vat()
        create_declarations_from_teleicare_history()
        CA_declaration = Declaration.objects.get(siccrf_id=CA.cplalim_ident)

        self.assertEqual(
            EtablissementToCompanyRelation.objects.filter(siccrf_id=etablissement_mandataire.etab_ident).count(), 0
        )
        self.assertEqual(CA_declaration.company, declarant_company)
        self.assertIsNone(CA_declaration.mandated_company)

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    def test_historic_declaration_is_updated_with_mandataire(self, mocked_add_composition_function):
        siret_declarant = _make_siret()
        etablissement_declarant = EtablissementFactory(etab_siret=siret_declarant)
        declarant_company = CompanyFactory(siret=siret_declarant)

        CA = ComplementAlimentaireFactory(etab=etablissement_declarant, frmgal_ident=self.galenic_formulation_id)
        CA_declaration = AuthorizedDeclarationFactory(company=declarant_company, siccrf_id=CA.cplalim_ident)

        self.assertIsNone(CA_declaration.mandated_company)
        self.assertEqual(Declaration.objects.all().count(), 1)

        siret_mandataire = _make_siret()
        etablissement_mandataire = EtablissementFactory(etab_siret=siret_mandataire)
        declaration = DeclarationFactory(
            cplalim=CA,
            etab=etablissement_mandataire,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        VersionDeclarationFactory(
            dcl=declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        match_companies_on_siret_or_vat(create_if_not_exist=True)

        create_declarations_from_teleicare_history(rewrite_existing=False)
        CA_declaration.refresh_from_db()
        self.assertIsNone(CA_declaration.mandated_company)

        create_declarations_from_teleicare_history(rewrite_existing=True)
        CA_declaration.refresh_from_db()
        self.assertEqual(Declaration.objects.all().count(), 1)
        self.assertTrue(EtablissementToCompanyRelation.objects.exclude(siccrf_id=None).exists())
        mandataire_company = EtablissementToCompanyRelation.objects.get(
            siccrf_id=etablissement_mandataire.etab_ident
        ).company  # les objets Company et EtablissementToCompanyRelation ont été créés
        self.assertEqual(CA_declaration.mandated_company, mandataire_company)

    @patch("data.etl.teleicare_history.extractor.add_composition_from_teleicare_history")
    def test_historic_declaration_has_been_assigned_to_other_company(self, mocked_add_composition_function):
        """
        Ce test permet de vérifier qu'une déclaration historiques qui aurait été assignée dans Compl'Alim à une nouvelle entreprise
        ne se retrouve pas avec sa company overwrite lors d'un nouvel import d'historique
        mais
        """
        siret_declarant = _make_siret()
        etablissement_declarant = EtablissementFactory(etab_siret=siret_declarant)
        declarant_company = CompanyFactory(siret=siret_declarant)

        CA = ComplementAlimentaireFactory(etab=etablissement_declarant, frmgal_ident=self.galenic_formulation_id)
        CA_declaration = AuthorizedDeclarationFactory(company=declarant_company, siccrf_id=CA.cplalim_ident)

        self.assertIsNone(CA_declaration.mandated_company)
        self.assertEqual(Declaration.objects.all().count(), 1)

        declaration = DeclarationFactory(
            cplalim=CA,
            tydcl_ident=1,
            dcl_date="03/20/2021 20:20:20 AM",
            dcl_date_fin_commercialisation=None,
        )
        VersionDeclarationFactory(
            dcl=declaration,
            stadcl_ident=8,
            stattdcl_ident=2,
            unt_ident=self.unit_id,
            vrsdecl_djr="32 kg of ppo",
        )
        match_companies_on_siret_or_vat(create_if_not_exist=True)

        # 1 ° import d'historique
        create_declarations_from_teleicare_history(rewrite_existing=False)
        CA_declaration.refresh_from_db()
        self.assertEqual(CA_declaration.company, declarant_company)

        # changement de company
        purchaser_company = CompanyFactory()
        CA_declaration.company = purchaser_company
        CA_declaration.save()
        self.assertEqual(CA_declaration.company, purchaser_company)

        # 2 ° import d'historique sans overwrite de la company
        create_declarations_from_teleicare_history(rewrite_existing=True)
        CA_declaration.refresh_from_db()
        self.assertEqual(CA_declaration.company, purchaser_company)
