from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PlantFactory


class TestElementsApi(APITestCase):
    def test_get_single_plant(self):
        plant = PlantFactory.create()
        response = self.client.get(reverse("single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(plant.name, body["name"])
        self.assertEqual(plant.id, body["id"])
