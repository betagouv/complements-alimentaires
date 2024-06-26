from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PopulationFactory


class TestPopulationApi(APITestCase):
    def test_get_population_list(self):
        """
        The API should return all non obsolete populations that are not missing data
        """
        complete_populations = [
            PopulationFactory.create(missing_import_data=False, is_obsolete=False) for i in range(3)
        ]
        incomplete_populations = [
            PopulationFactory.create(missing_import_data=True, is_obsolete=False) for i in range(2)
        ]
        obsolete_populations = [PopulationFactory.create(missing_import_data=True, is_obsolete=True) for i in range(3)]
        response = self.client.get(reverse("api:population_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for population in complete_populations:
            self.assertTrue(any(x["id"] == population.id for x in body))

        for population in incomplete_populations:
            self.assertFalse(any(x["id"] == population.id for x in body))

        for population in obsolete_populations:
            self.assertFalse(any(x["id"] == population.id for x in body))
