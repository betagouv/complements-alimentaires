from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import (
    PlantFactory,
    PlantSynonymFactory,
    IngredientFactory,
    SubstanceFactory,
)


class TestAutocomplete(APITestCase):
    def test_missing_autocomplete_term(self):
        """
        A missing autocomplete term is considered a bad request
        """
        response = self.client.post(f"{reverse('substance_autocomplete')}", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_autocomplete_term(self):
        """
        A autocomplete term of less than three chars is considered a bad request
        """
        response = self.client.post(f"{reverse('substance_autocomplete')}", {"search": "ab"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_autocomplete_name(self):
        """
        Simple single-class name test
        """
        autocomplete_term = "eucal"

        # Devrait apparaître en première position à cause de son score SequenceMatcher
        eucalyptus_1 = SubstanceFactory.create(name="eucalyptus")

        # Deuxième position car la chaîne de caractères est plus éloignée
        eucalyptus_2 = IngredientFactory.create(name="eucalyptus tree")

        # Troisième position grâce à son synonyme de nom « "Eucalyptus Plant" »
        myrtaceae = PlantFactory.create(name="Myrtaceae")
        PlantSynonymFactory.create(name="Eucalyptus Plant", standard_name=myrtaceae)

        # Ne devrait pas apparaître
        PlantFactory.create(name="vanille")

        response = self.client.post(f"{reverse('substance_autocomplete')}", {"term": autocomplete_term})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()

        returned_ids = [result.get("id") for result in results]
        self.assertEqual(len(returned_ids), 3)
        self.assertEqual(returned_ids[0], eucalyptus_1.id)
        self.assertEqual(returned_ids[1], eucalyptus_2.id)
        self.assertEqual(returned_ids[2], myrtaceae.id)
