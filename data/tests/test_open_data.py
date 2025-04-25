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
    MicroorganismFactory,
    PlantFactory,
    PlantPartFactory,
    SubstanceFactory,
    SubstanceUnitFactory,
)
from data.models import Declaration


class IngredientTestCase(TestCase):
    @mock.patch("data.etl.datagouv.update_resources")
    def test_created_csv_is_json_compliant(self, mocked_update_resources):
        """
        Le fichier csv créé à la sortie du process d'extraction du JDD Open Data contient des colonnes de données complexes qui sont en json bien formé
        """
        # Création de declarations dont déclarations provenant de TeleIcare
        declaration_1 = AuthorizedDeclarationFactory()
        DeclaredPlantFactory(
            declaration=declaration_1,
            plant=PlantFactory(name="Ortie"),
            used_part=PlantPartFactory(ca_name="Parties aériennes"),
            quantity=5.0,
            unit=SubstanceUnitFactory(name="mg"),
        )
        declaration_2 = AuthorizedDeclarationFactory()
        declaration_2.declared_substances.set([])
        substance = SubstanceFactory(ca_name="Vitamine C")
        DeclaredSubstanceFactory(
            declaration=declaration_2,
            substance=substance,
            quantity=10.0,
            unit=SubstanceUnitFactory(name="mg"),
        )
        declaration_teleicare = AuthorizedDeclarationFactory(siccrf_id=567365, teleicare_id="2025-06-07")
        DeclaredMicroorganismFactory(
            declaration=declaration_teleicare,
            microorganism=MicroorganismFactory(ca_genus="Lactobasine", ca_species="en bois"),
            quantity=5.0,
        )
        AwaitingInstructionDeclarationFactory()
        self.assertEqual(Declaration.objects.all().count(), 4)

        # default_storage est FileSystemStorage dans l'environnement de test
        etl_test = ETL_OPEN_DATA_DECLARATIONS()
        etl_test.dataset_name = "test_declarations"
        etl_test.extract_dataset()
        etl_test.transform_dataset()
        etl_test.load_dataset()

        open_data_jdd = pd.read_csv(os.path.join(settings.MEDIA_ROOT, etl_test.dataset_name + ".csv"), delimiter=";")
        self.assertEqual(len(open_data_jdd), 3)
        substance_loaded = json.loads(open_data_jdd["substances"][1])
        self.assertEqual(substance_loaded[3]["nom"], "Vitamine C")
        self.assertEqual(substance_loaded[3]["unite"], "mg")

        # supprime le fichier qui vient d'être créé
        default_storage.delete(etl_test.dataset_name + ".csv")
