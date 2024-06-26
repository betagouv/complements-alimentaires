from rest_framework import status

from .utils import ProjectAPITestCase
from data.factories import GalenicFormulationFactory


class TestGalenicFormulationApi(ProjectAPITestCase):
    viewname = "galenic_formulation_list"

    def test_get_galenic_formulation_list(self):
        """
        The API should return all non obsolete galenicFormulation that are not missing data
        """

        complete_formulations = [
            GalenicFormulationFactory.create(missing_import_data=False, siccrf_is_obsolete=False, ca_is_obsolete=False)
            for i in range(3)
        ]
        incomplete_formulations = [
            GalenicFormulationFactory.create(missing_import_data=True, siccrf_is_obsolete=False, ca_is_obsolete=False)
            for i in range(2)
        ]
        obsolete_formulations = [
            GalenicFormulationFactory.create(missing_import_data=True, siccrf_is_obsolete=True, ca_is_obsolete=True)
            for i in range(3)
        ]
        response = self.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for formulation in complete_formulations:
            self.assertTrue(any(x["id"] == formulation.id for x in body))

        for formulation in incomplete_formulations:
            self.assertFalse(any(x["id"] == formulation.id for x in body))

        for formulation in obsolete_formulations:
            self.assertFalse(any(x["id"] == formulation.id for x in body))
