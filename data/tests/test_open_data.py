import json
import os
from unittest import mock

from django.conf import settings
from django.core.files.storage import default_storage
from django.test import TestCase
from django.test.utils import override_settings

import pandas as pd

from data.etl.declarations import OpenDataDeclarationsETL
from data.factories import (
    AuthorizedDeclarationFactory,
    AwaitingInstructionDeclarationFactory,
    DeclaredMicroorganismFactory,
    DeclaredPlantFactory,
    DeclaredSubstanceFactory,
    InstructionReadyDeclarationFactory,
    MicroorganismFactory,
    ObjectionDeclarationFactory,
    ObservationDeclarationFactory,
    OngoingInstructionDeclarationFactory,
    PlantFactory,
    PlantPartFactory,
    SubstanceFactory,
    SubstanceUnitFactory,
)
from data.models import Declaration


class IngredientTestCase(TestCase):
    def setUp(self):
        # default_storage est FileSystemStorage dans l'environnement de test

        self.etl_test = OpenDataDeclarationsETL()
        self.etl_test.dataset_name = "test_declarations"

    def tearDown(self):
        # supprime le fichier qui vient d'être créé
        if default_storage.exists(self.etl_test.filename):
            default_storage.delete(self.etl_test.filename)

    @override_settings(DECLARATIONS_EXPORT_BATCH_SIZE=1)
    def test_declaration_jdd_contains_only_authorized_declarations(self):
        AuthorizedDeclarationFactory()
        AwaitingInstructionDeclarationFactory()
        InstructionReadyDeclarationFactory()
        OngoingInstructionDeclarationFactory()
        ObservationDeclarationFactory()
        ObjectionDeclarationFactory()

        self.assertEqual(Declaration.objects.all().count(), 6)

        # tester l'export avec un taille de batch d'une déclaration
        self.etl_test.export()

        open_data_jdd = pd.read_csv(os.path.join(settings.MEDIA_ROOT, self.etl_test.filename), delimiter=";")
        self.assertEqual(len(open_data_jdd), 1)

    @override_settings(DECLARATIONS_EXPORT_BATCH_SIZE=1)
    @mock.patch("data.etl.datagouv.update_resources")
    def test_created_csv_is_json_compliant(self, mocked_update_resources):
        """
        Le fichier csv créé à la sortie du process d'extraction du JDD Open Data contient des colonnes de données complexes qui sont en json bien formé
        """
        # Création de declarations dont déclarations provenant de TeleIcare
        unit_mg = SubstanceUnitFactory(name="mg")
        declaration_1 = AuthorizedDeclarationFactory()
        DeclaredPlantFactory(
            declaration=declaration_1,
            plant=PlantFactory(name="Ortie"),
            used_part=PlantPartFactory(name="Parties aériennes"),
            quantity=5.0,
            unit=unit_mg,
        )
        declaration_2 = AuthorizedDeclarationFactory(declared_substances=[])
        substance = SubstanceFactory(name="Vitamine C")
        DeclaredSubstanceFactory(
            declaration=declaration_2,
            substance=substance,
            quantity=10.0,
            unit=unit_mg,
        )
        declaration_teleicare = AuthorizedDeclarationFactory(
            siccrf_id=567365, teleicare_declaration_number="2025-06-07"
        )
        DeclaredMicroorganismFactory(
            declaration=declaration_teleicare,
            microorganism=MicroorganismFactory(genus="Lactobasine", species="en bois"),
            quantity=5.0,
        )

        # tester l'export avec un taille de batch d'une déclaration
        self.etl_test.export()

        open_data_jdd = pd.read_csv(os.path.join(settings.MEDIA_ROOT, self.etl_test.filename), delimiter=";")
        self.assertEqual(len(open_data_jdd), 3)

        def is_vitamin_c(substance):
            json_substance = json.loads(substance)
            return "nom" in json_substance[0] and json_substance[0]["nom"] == "Vitamine C"

        substance_loaded = json.loads(next(x for x in open_data_jdd["substances"] if is_vitamin_c(x)))
        self.assertEqual(substance_loaded[0]["quantité_par_djr"], 10)
        self.assertEqual(substance_loaded[0]["unite"], "mg")
