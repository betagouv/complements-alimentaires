from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PlantFactory, IngredientFactory, SubstanceFactory, MicroorganismFactory


class TestSearch(APITestCase):
    def test_missing_search_term(self):
        """
        A missing search term is considered a bad request
        """
        response = self.client.post(f"{reverse('search')}", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_search_term(self):
        """
        A search term of less than three chars is considered a bad request
        """
        response = self.client.post(f"{reverse('search')}", {"search": "ab"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_name(self):
        """
        Simple single-class name test
        """
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

    def test_search_multiple_tables(self):
        """
        Multiple-class name test
        """
        plant = PlantFactory.create(name="matcha latte")
        ingredient = IngredientFactory.create(name="matcha powder")
        substance = SubstanceFactory.create(name="cafe latte")
        microorganism = MicroorganismFactory.create(name="cafe powder")

        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results, count = response.json().get("results", []), response.json().get("count")

        self.assertEqual(count, 2)
        returned_ids = [result.get("id") for result in results]
        self.assertIn(plant.id, returned_ids)
        self.assertIn(ingredient.id, returned_ids)

        search_term = "cafe"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results, count = response.json().get("results", []), response.json().get("count")

        self.assertEqual(count, 2)
        returned_ids = [result.get("id") for result in results]
        self.assertIn(substance.id, returned_ids)
        self.assertIn(microorganism.id, returned_ids)

        search_term = "powder"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results, count = response.json().get("results", []), response.json().get("count")

        self.assertEqual(count, 2)
        returned_ids = [result.get("id") for result in results]
        self.assertIn(ingredient.id, returned_ids)
        self.assertIn(microorganism.id, returned_ids)

    def test_ingredient_field_priorities(self):
        """
        The weighting of certain fields yields different scores. For example,
        an ingredients `name` has a higher search priority than its `name_en`
        which has a higher priority than its `description`
        """
        ingredient_description = IngredientFactory(description="matcha")
        ingredient_name = IngredientFactory(name="matcha")
        ingredient_name_en = IngredientFactory(name_en="matcha")

        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results = response.json().get("results", [])

        self.assertEqual(results[0]["id"], ingredient_name.id)
        self.assertEqual(results[1]["id"], ingredient_name_en.id)
        self.assertEqual(results[2]["id"], ingredient_description.id)
