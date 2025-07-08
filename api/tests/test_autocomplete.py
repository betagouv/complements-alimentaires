from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    IngredientFactory,
    MicroorganismFactory,
    MicroorganismSynonymFactory,
    PlantFactory,
    PlantSynonymFactory,
    SubstanceFactory,
    SubstanceSynonymFactory,
)
from data.models.ingredient_status import IngredientStatus
from data.models.substance import SubstanceType


class TestAutocomplete(APITestCase):
    def test_missing_autocomplete_term(self):
        """
        A missing autocomplete term is considered a bad request
        """
        response = self.client.post(f"{reverse('api:element_autocomplete')}", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_autocomplete_term(self):
        """
        A autocomplete term of less than three chars is considered a bad request
        """
        response = self.client.post(f"{reverse('api:element_autocomplete')}", {"term": "ab"})
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
        eucalyptus_1 = SubstanceFactory.create(name="eucalyptus", substance_types=[SubstanceType.BIOACTIVE_SUBSTANCE])

        # Deuxième position car la chaîne de caractères est plus éloignée
        eucalyptus_2 = IngredientFactory.create(name="eucalyptus tree")

        # Troisième position grâce à son synonyme de nom « "Eucalyptus Plant" »
        myrtaceae = PlantFactory.create(name="Myrtaceae")
        PlantSynonymFactory.create(name="Eucalyptus Plant", standard_name=myrtaceae)

        # Ne devrait pas apparaître
        PlantFactory.create(name="vanille")

        response = self.client.post(f"{reverse('api:element_autocomplete')}", {"term": autocomplete_term})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()

        returned_ids = [result.get("id") for result in results]
        self.assertEqual(len(returned_ids), 3)
        self.assertEqual(returned_ids[0], eucalyptus_1.id)
        self.assertEqual(returned_ids[1], eucalyptus_2.id)
        self.assertEqual(returned_ids[2], myrtaceae.id)

        self.assertEqual(results[0]["objectType"], "substance")
        self.assertEqual(results[1]["objectType"], "active_ingredient")
        self.assertEqual(results[2]["objectType"], "plant")

    def test_autocomplete_accented(self):
        """
        Accents should not impact query
        """
        autocomplete_term = "buplevre"

        # Devrait apparaître en première position à cause de son score SequenceMatcher
        buplevre_1 = SubstanceFactory.create(name="Buplèvre", substance_types=[SubstanceType.BIOACTIVE_SUBSTANCE])

        # Deuxième position car la chaîne de caractères est plus éloignée
        buplevre_2 = PlantFactory.create(name="Buplèvre en faux")

        # Troisième position grâce à son synonyme de nom « "Buplèvre à feuilles rondes" »
        pancic = MicroorganismFactory.create(name="Pančić")
        MicroorganismSynonymFactory.create(name="Buplèvre à feuilles rondes", standard_name=pancic)

        # Ne devrait pas apparaître
        PlantFactory.create(name="vanille")

        response = self.client.post(f"{reverse('api:element_autocomplete')}", {"term": autocomplete_term})
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
        Elements with status "Non autorisé" should not be returned by autocomplete except Plants
        """
        autocomplete_term = "ephedra"

        # Devrait apparaître en première position à cause de son score SequenceMatcher
        authorized_substance = SubstanceFactory.create(
            name="Vitamine C",
            status=IngredientStatus.AUTHORIZED,
            substance_types=[SubstanceType.BIOACTIVE_SUBSTANCE],
        )
        SubstanceSynonymFactory.create(name="Ephedra", standard_name=authorized_substance)

        forbidden_plant = PlantFactory.create(name="Ephedra sepervirens", status=IngredientStatus.NOT_AUTHORIZED)
        forbidden_ingredient = IngredientFactory.create(
            name="Ephedra ingredient", status=IngredientStatus.NOT_AUTHORIZED
        )
        forbidden_substance = SubstanceFactory.create(
            name="Ephedra ine",
            status=IngredientStatus.NOT_AUTHORIZED,
            substance_types=[SubstanceType.BIOACTIVE_SUBSTANCE],
        )

        to_be_authorized_plant = PlantFactory.create(
            name="Ephedralite", status=IngredientStatus.AUTHORIZED, to_be_entered_in_next_decree=True
        )

        response = self.client.post(f"{reverse('api:element_autocomplete')}", {"term": autocomplete_term})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        returned_names = [result.get("name") for result in results]

        self.assertFalse(forbidden_ingredient.name in returned_names)
        self.assertFalse(forbidden_substance.name in returned_names)
        self.assertTrue(forbidden_plant.name in returned_names)
        self.assertTrue(authorized_substance.name in returned_names)
        self.assertTrue(to_be_authorized_plant.name in returned_names)
        self.assertEqual(len(returned_names), 3)

        # Si la requête demande explicitement l'inclusion de touts les élémenets on aura bien cinq
        # résultats
        response = self.client.post(
            f"{reverse('api:element_autocomplete')}", {"term": autocomplete_term, "all": "true"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertEqual(len(results), 5)
        returned_names = [result.get("name") for result in results]

        self.assertTrue(forbidden_ingredient.name in returned_names)
        self.assertTrue(forbidden_substance.name in returned_names)

    def test_only_return_bioactive_substances(self):
        """
        Les substances qui ont le type "MINERAL" ou "VITAMINE" ou "SECONDARY_METABOLITE" ou "OTHER_BIOACTIVE_SUBSTANCE"
        sans être accompagné du type "BIOACTIVE_SUBSTANCE" ne devraient pas être retournées par l'autocomplete
        """
        # Création des ingrédients
        substance_to_be_returned_1 = SubstanceFactory.create(
            name="Vitamine A",
            status=IngredientStatus.AUTHORIZED,
            substance_types=[SubstanceType.VITAMIN, SubstanceType.BIOACTIVE_SUBSTANCE],
        )
        substance_to_be_returned_2 = SubstanceFactory.create(
            name="Vitamine B",
            status=IngredientStatus.AUTHORIZED,
            substance_types=[SubstanceType.BIOACTIVE_SUBSTANCE],
        )
        _ = SubstanceFactory.create(
            name="Vitamine C", status=IngredientStatus.AUTHORIZED, substance_types=[SubstanceType.VITAMIN]
        )

        _ = SubstanceFactory.create(name="Vitamine RAS", status=IngredientStatus.AUTHORIZED, substance_types=[])

        autocomplete_term = "vitamine"

        response = self.client.post(f"{reverse('api:element_autocomplete')}", {"term": autocomplete_term})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        returned_names = [result.get("name") for result in results]

        self.assertTrue(substance_to_be_returned_2.name in returned_names)
        self.assertTrue(substance_to_be_returned_1.name in returned_names)
        self.assertEqual(len(returned_names), 2)

        # Si la requête demande explicitement l'inclusion de touts les élémenets on aura bien quatre
        # résultats
        response = self.client.post(
            f"{reverse('api:element_autocomplete')}", {"term": autocomplete_term, "all": "true"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertEqual(len(results), 4)

    def test_autocomplete_filtered_by_type(self):
        """
        On peut filtrer les résultats par type
        """
        autocomplete_term = "eucal"

        # Devrait apparaître en première position à cause de son score SequenceMatcher
        eucalyptus_1 = SubstanceFactory.create(name="eucalyptus", substance_types=[SubstanceType.BIOACTIVE_SUBSTANCE])

        # ne pas faire apparaître
        IngredientFactory.create(name="eucalyptus tree")

        response = self.client.post(
            f"{reverse('api:element_autocomplete')}", {"term": autocomplete_term, "type": "substance"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()

        returned_ids = [result.get("id") for result in results]
        self.assertEqual(len(returned_ids), 1)
        self.assertEqual(returned_ids[0], eucalyptus_1.id)
        self.assertEqual(results[0]["objectType"], "substance")
