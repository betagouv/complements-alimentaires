from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    IngredientFactory,
    InstructionRoleFactory,
    MicroorganismFactory,
    PlantFactory,
    PlantPartFactory,
    SubstanceFactory,
)
from data.models import IngredientType

from .utils import authenticate


class TestElementsApi(APITestCase):
    def test_get_single_plant(self):
        plant = PlantFactory.create()
        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(plant.name, body["name"])
        self.assertEqual(plant.id, body["id"])

    @authenticate
    def test_plant_private_comments(self):
        plant = PlantFactory.create(private_comments="Private")
        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertNotIn("privateComments", body)

        # On les affiche si on a un rôle dans l'administration
        InstructionRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertIn("privateComments", body)

    @authenticate
    def test_ingredient_private_comments(self):
        ingredient = IngredientFactory.create()

        # Si on ne fait pas partie de l'administration on ne montre pas les commentaires privés
        response = self.client.get(reverse("api:single_ingredient", kwargs={"pk": ingredient.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertNotIn("privateComments", body)

        # On les affiche si on a un rôle dans l'administration
        InstructionRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:single_ingredient", kwargs={"pk": ingredient.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertIn("privateComments", body)

    def test_get_single_ingredient(self):
        ingredient = IngredientFactory.create(private_comments="private")
        response = self.client.get(reverse("api:single_ingredient", kwargs={"pk": ingredient.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(ingredient.name, body["name"])
        self.assertEqual(ingredient.id, body["id"])

    def test_get_single_ingredient_with_right_type(self):
        """
        Le modèle (table) ingrédient à un champ `ingredient_type`.
        C'est la même route api qui sert les différents types.
        On vérifie ici que le type est bien retourné.
        """
        active_ingredient = IngredientFactory.create(ingredient_type=IngredientType.ACTIVE_INGREDIENT)
        response = self.client.get(reverse("api:single_ingredient", kwargs={"pk": active_ingredient.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result1 = response.json()
        self.assertEqual(result1["objectType"], "active_ingredient")

        aroma = IngredientFactory.create(ingredient_type=IngredientType.AROMA)
        response = self.client.get(reverse("api:single_ingredient", kwargs={"pk": aroma.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result2 = response.json()
        self.assertEqual(result2["objectType"], "aroma")

        additive = IngredientFactory.create(ingredient_type=IngredientType.ADDITIVE)
        response = self.client.get(reverse("api:single_ingredient", kwargs={"pk": additive.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result2 = response.json()
        self.assertEqual(result2["objectType"], "additive")

    def test_get_single_microorganism(self):
        microorganism = MicroorganismFactory.create()
        response = self.client.get(reverse("api:single_microorganism", kwargs={"pk": microorganism.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(microorganism.name, body["name"])
        self.assertEqual(microorganism.id, body["id"])

    @authenticate
    def test_microorganism_private_comments(self):
        microorganism = MicroorganismFactory.create(private_comments="private")
        response = self.client.get(reverse("api:single_microorganism", kwargs={"pk": microorganism.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("privateComments", body)

        # On les affiche si on a un rôle dans l'administration
        InstructionRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:single_microorganism", kwargs={"pk": microorganism.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertIn("privateComments", body)

    def test_get_single_substance(self):
        substance = SubstanceFactory.create()
        response = self.client.get(reverse("api:single_substance", kwargs={"pk": substance.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(substance.name, body["name"])
        self.assertEqual(substance.id, body["id"])

    @authenticate
    def test_substance_private_comments(self):
        substance = SubstanceFactory.create()
        response = self.client.get(reverse("api:single_substance", kwargs={"pk": substance.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertNotIn("privateComments", body)

        # On les affiche si on a un rôle dans l'administration
        InstructionRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:single_substance", kwargs={"pk": substance.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertIn("privateComments", body)

    def test_get_plant_parts(self):
        part_1 = PlantPartFactory.create()
        part_2 = PlantPartFactory.create()
        response = self.client.get(reverse("api:plant_part_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 2)
        self.assertIsNotNone(filter(lambda x: x["id"] == part_1.id, body))
        self.assertIsNotNone(filter(lambda x: x["id"] == part_2.id, body))
