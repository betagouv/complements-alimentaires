from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.models.status import IngredientStatus
from data.factories import (
    PlantFactory,
    PlantSynonymFactory,
    IngredientFactory,
    SubstanceFactory,
    SubstanceSynonymFactory,
    MicroorganismFactory,
    MicroorganismSynonymFactory,
)


class TestAutocomplete(APITestCase):
    def test_missing_autocomplete_term(self):
        """
        A missing autocomplete term is considered a bad request
        """
        response = self.client.post(f"{reverse('api:substance_autocomplete')}", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_autocomplete_term(self):
        """
        A autocomplete term of less than three chars is considered a bad request
        """
        response = self.client.post(f"{reverse('api:substance_autocomplete')}", {"term": "ab"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["globalError"], "Le terme de recherche doit être supérieur ou égal à 3 caractères"
        )

    def test_autocomplete_name(self):
        """
        Simple single-class name test
        """
        autocomplete_term = "eucal"

        # Devrait apparaître en première position à cause de son score SequenceMatcher
        eucalyptus_1 = SubstanceFactory.create(ca_name="eucalyptus")

        # Deuxième position car la chaîne de caractères est plus éloignée
        eucalyptus_2 = IngredientFactory.create(ca_name="eucalyptus tree")

        # Troisième position grâce à son synonyme de nom « "Eucalyptus Plant" »
        myrtaceae = PlantFactory.create(ca_name="Myrtaceae")
        PlantSynonymFactory.create(name="Eucalyptus Plant", standard_name=myrtaceae)

        # Ne devrait pas apparaître
        PlantFactory.create(ca_name="vanille")

        response = self.client.post(f"{reverse('api:substance_autocomplete')}", {"term": autocomplete_term})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()

        returned_ids = [result.get("id") for result in results]
        self.assertEqual(len(returned_ids), 3)
        self.assertEqual(returned_ids[0], eucalyptus_1.id)
        self.assertEqual(returned_ids[1], eucalyptus_2.id)
        self.assertEqual(returned_ids[2], myrtaceae.id)

        self.assertEqual(results[0]["objectType"], "substance")
        self.assertEqual(results[1]["objectType"], "ingredient")
        self.assertEqual(results[2]["objectType"], "plant")

    def test_autocomplete_accented(self):
        """
        Accents should not impact query
        """
        autocomplete_term = "buplevre"

        # Devrait apparaître en première position à cause de son score SequenceMatcher
        buplevre_1 = SubstanceFactory.create(ca_name="Buplèvre")

        # Deuxième position car la chaîne de caractères est plus éloignée
        buplevre_2 = PlantFactory.create(ca_name="Buplèvre en faux")

        # Troisième position grâce à son synonyme de nom « "Buplèvre à feuilles rondes" »
        pancic = MicroorganismFactory.create(name="Pančić")
        MicroorganismSynonymFactory.create(name="Buplèvre à feuilles rondes", standard_name=pancic)

        # Ne devrait pas apparaître
        PlantFactory.create(ca_name="vanille")

        response = self.client.post(f"{reverse('api:substance_autocomplete')}", {"term": autocomplete_term})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()

        returned_ids = [result.get("id") for result in results]
        self.assertEqual(len(returned_ids), 3)
        self.assertEqual(returned_ids[0], buplevre_1.id)
        self.assertEqual(returned_ids[1], buplevre_2.id)
        self.assertEqual(returned_ids[2], pancic.id)

        self.assertEqual(results[0]["objectType"], "substance")
        self.assertEqual(results[1]["objectType"], "plant")
        self.assertEqual(results[2]["objectType"], "microorganism")

    def test_status_of_autocomplete_result(self):
        """
        Elements with status "Non autorisé" should not be returned by autocomplete
        """
        autocomplete_term = "ephedra"

        # Devrait apparaître en première position à cause de son score SequenceMatcher
        authorized_substance = SubstanceFactory.create(ca_name="Vitamine C", status=IngredientStatus.AUTHORIZED)
        SubstanceSynonymFactory.create(name="Ephedra", standard_name=authorized_substance)

        forbidden_plant = PlantFactory.create(ca_name="Ephedra", status=IngredientStatus.NOT_AUTHORIZED)

        to_be_authorized_plant = PlantFactory.create(
            ca_name="Ephedralite", status=IngredientStatus.PENDING_REGISTRATION
        )

        response = self.client.post(f"{reverse('api:substance_autocomplete')}", {"term": autocomplete_term})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        returned_names = [result.get("name") for result in results]

        self.assertFalse(forbidden_plant.name in returned_names)
        self.assertTrue(authorized_substance.name in returned_names)
        self.assertTrue(to_be_authorized_plant.name in returned_names)
        self.assertEqual(len(returned_names), 2)
