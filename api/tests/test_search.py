from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import (
    PlantFactory,
    IngredientFactory,
    IngredientSynonymFactory,
    SubstanceFactory,
    SubstanceSynonymFactory,
    MicroorganismFactory,
    MicroorganismSynonymFactory,
)


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

    def test_max_limit(self):
        """
        The pagination limit must not be exceeded
        """
        response = self.client.post(f"{reverse('search')}", {"search": "abc", "limit": 49})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_name(self):
        """
        Simple single-class name test
        """
        eucalyptus_1 = PlantFactory.create(ca_name="eucalyptus")
        eucalyptus_2 = PlantFactory.create(ca_name="eucalyptus")
        vanille = PlantFactory.create(ca_name="vanille")

        search_term = "eucalyptus"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        returned_ids = [result.get("id") for result in results]
        self.assertNotIn(vanille.id, returned_ids)
        self.assertIn(eucalyptus_1.id, returned_ids)
        self.assertIn(eucalyptus_2.id, returned_ids)

    def test_search_synonym(self):
        """Simple synonym test"""
        IngredientSynonymFactory(name="matcha", standard_name=IngredientFactory(ca_name="other"))
        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results = response.json().get("results", [])
        self.assertTrue("other" in [result["name"] for result in results])

    def test_search_multiple_tables(self):
        """
        Multiple-class name test
        """
        plant = PlantFactory.create(ca_name="matcha latte")
        ingredient = IngredientFactory.create(ca_name="matcha powder")
        substance = SubstanceFactory.create(ca_name="cafe latte")
        microorganism = MicroorganismFactory.create(ca_genus="cafe", ca_species="powder")

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
        an ingredients `name` has a higher search priority than its `name_en` and `ingredientsynonym`
        which has a higher priority than its `description`
        """
        ingredient_name = IngredientFactory(ca_name="matcha")
        IngredientSynonymFactory(name="matcha", standard_name=IngredientFactory(ca_name="other"))
        IngredientFactory(siccrf_name_en="matcha")
        ingredient_description = IngredientFactory(siccrf_description="matcha")

        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results = response.json().get("results", [])
        self.assertEqual(results[0]["id"], ingredient_name.id)
        self.assertEqual(results[3]["id"], ingredient_description.id)

    def test_microorganism_field_priorities(self):
        """
        The weighting of certain fields yields different scores. For example,
        a microorganism `name` has a higher search priority than `microorganismsynonym`
        """
        microorganism_name = MicroorganismFactory(ca_genus="matcha")
        microorganism_synonym = MicroorganismFactory(ca_genus="other")
        MicroorganismSynonymFactory(name="matcha", standard_name=microorganism_synonym)

        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results = response.json().get("results", [])

        self.assertEqual(results[0]["id"], microorganism_name.id)
        self.assertEqual(results[1]["id"], microorganism_synonym.id)

    def test_substance_field_priorities(self):
        """
        The weighting of certain fields yields different scores. For example,
        a substance `name`, `cas_number` and `einec_number` have a higher search
        priority than its `name_en` and `substancesynonym`
        """
        substance_name_en = SubstanceFactory(siccrf_name_en="matcha")
        substance_synonym = SubstanceFactory(ca_name="other")
        SubstanceSynonymFactory(name="matcha", standard_name=substance_synonym)
        SubstanceFactory(siccrf_cas_number="matcha")
        SubstanceFactory(siccrf_einec_number="matcha")
        SubstanceFactory(ca_name="matcha")

        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results = response.json().get("results", [])

        two_last_results = [result["id"] for result in results[-2:]]
        self.assertIn(substance_name_en.id, two_last_results)
        self.assertIn(substance_synonym.id, two_last_results)

    def test_multiple_microorganism_synonym_match_return_only_once(self):
        """The search_term might be found in several fields,
        in this case, the object should appear only once in search results
        """
        moorg = MicroorganismFactory(ca_genus="matcha")
        MicroorganismSynonymFactory(name="matcha latte", standard_name=moorg)
        MicroorganismSynonymFactory(name="boisson matcha", standard_name=moorg)

        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results = response.json().get("results", [])

        self.assertEqual(len(results), 1)

    def test_multiple_substance_synonym_match_return_only_once(self):
        """The search_term might be found in several fields,
        in this case, the object should appear only once in search results
        """
        substance = SubstanceFactory(ca_name="matcha")
        SubstanceSynonymFactory(name="matcha latte", standard_name=substance)
        SubstanceSynonymFactory(name="boisson matcha", standard_name=substance)

        search_term = "matcha"
        response = self.client.post(f"{reverse('search')}", {"search": search_term})
        results = response.json().get("results", [])

        self.assertEqual(len(results), 1)

    def test_pagination(self):
        """
        Pagination is controlled by parameters `limit` and `offset`
        """
        for i in range(9):
            PlantFactory.create(ca_name="matcha")

        search_term = "matcha"

        response_page_1 = self.client.post(f"{reverse('search')}", {"search": search_term, "limit": 5, "offset": 0})
        page_1_ids = [result["id"] for result in response_page_1.json().get("results", [])]
        self.assertEqual(len(page_1_ids), 5)

        response_page_2 = self.client.post(f"{reverse('search')}", {"search": search_term, "limit": 5, "offset": 5})
        page_2_ids = [result["id"] for result in response_page_2.json().get("results", [])]
        self.assertEqual(len(page_2_ids), 4)

        for id in page_1_ids:
            self.assertNotIn(id, page_2_ids)
