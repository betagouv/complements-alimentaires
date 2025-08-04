import json
import os
from unittest import mock

from django.conf import settings
from django.core.files.storage import default_storage
from django.test import TestCase

import pandas as pd

from data.etl.transformer_loader import ETL_OPEN_DATA_DECLARATIONS
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

        self.etl_test = ETL_OPEN_DATA_DECLARATIONS()
        self.etl_test.dataset_name = "test_declarations"

    def test_declaration_jdd_contains_only_authorized_declarations(self):
        AuthorizedDeclarationFactory()
        AwaitingInstructionDeclarationFactory()
        InstructionReadyDeclarationFactory()
        OngoingInstructionDeclarationFactory()
        ObservationDeclarationFactory()
        ObjectionDeclarationFactory()

        self.assertEqual(Declaration.objects.all().count(), 6)

        self.etl_test.extract_dataset()
        self.etl_test.transform_dataset()
        self.etl_test.load_dataset()

        open_data_jdd = pd.read_csv(
            os.path.join(settings.MEDIA_ROOT, self.etl_test.dataset_name + ".csv"), delimiter=";"
        )
        self.assertEqual(len(open_data_jdd), 1)

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

        self.etl_test.extract_dataset()
        self.etl_test.transform_dataset()
        self.etl_test.load_dataset()

        open_data_jdd = pd.read_csv(
            os.path.join(settings.MEDIA_ROOT, self.etl_test.dataset_name + ".csv"), delimiter=";"
        )
        self.assertEqual(len(open_data_jdd), 3)

        def is_vitamin_c(substance):
            json_substance = json.loads(substance)
            return "nom" in json_substance[0] and json_substance[0]["nom"] == "Vitamine C"

        substance_loaded = json.loads(next(x for x in open_data_jdd["substances"] if is_vitamin_c(x)))
        self.assertEqual(substance_loaded[0]["quantité_par_djr"], 10)
        self.assertEqual(substance_loaded[0]["unite"], "mg")

        # supprime le fichier qui vient d'être créé
        default_storage.delete(self.etl_test.dataset_name + ".csv")
