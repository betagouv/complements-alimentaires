from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PlantFactory, IngredientFactory, MicroorganismFactory


class TestElementsApi(APITestCase):
    def test_get_single_plant(self):
        plant = PlantFactory.create()
        response = self.client.get(reverse("single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(plant.name, body["name"])
        self.assertEqual(plant.id, body["id"])

    def test_get_single_ingredient(self):
        ingredient = IngredientFactory.create()
        response = self.client.get(reverse("single_ingredient", kwargs={"pk": ingredient.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(ingredient.name, body["name"])
        self.assertEqual(ingredient.id, body["id"])

    def test_get_single_microorganism(self):
        microorganism = MicroorganismFactory.create()
        response = self.client.get(reverse("single_microorganism", kwargs={"pk": microorganism.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(microorganism.name, body["name"])
        self.assertEqual(microorganism.id, body["id"])
