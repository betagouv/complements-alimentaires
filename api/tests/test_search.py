from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PlantFactory


class TestSearch(APITestCase):
    def test_search_name(self):
        eucalyptus_1 = PlantFactory.create(name="eucalyptus")
        eucalyptus_2 = PlantFactory.create(name="eucalyptus")
        vanille = PlantFactory.create(name="vanille")

        search_term = "eucalyptus"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        returned_ids = [result.get("id") for result in results]
        self.assertNotIn(vanille.id, returned_ids)
        self.assertIn(eucalyptus_1.id, returned_ids)
        self.assertIn(eucalyptus_2.id, returned_ids)
