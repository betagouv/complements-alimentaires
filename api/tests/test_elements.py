from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    IngredientFactory,
    InstructionRoleFactory,
    MicroorganismFactory,
    PlantFactory,
    PlantPartFactory,
    PlantFamilyFactory,
    SubstanceFactory,
)
from data.models import IngredientType, Plant, IngredientStatus, Microorganism

from .utils import authenticate


class TestElementsFetchApi(APITestCase):
    def test_get_single_plant(self):
        plant = PlantFactory.create()
        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(plant.name, body["name"])
        self.assertEqual(plant.id, body["id"])

    def test_get_single_plant_history(self):
        plant = PlantFactory.create()
        response = self.client.get(f"{reverse('api:single_plant', kwargs={'pk': plant.id})}?history=true")
        body = response.json()

        self.assertIn("history", body)

        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        body = response.json()

        self.assertNotIn("history", body)

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

    def test_get_single_ingredient_history(self):
        ingredient = IngredientFactory.create()
        response = self.client.get(f"{reverse('api:single_ingredient', kwargs={'pk': ingredient.id})}?history=true")
        body = response.json()

        self.assertIn("history", body)

        response = self.client.get(reverse("api:single_ingredient", kwargs={"pk": ingredient.id}))
        body = response.json()

        self.assertNotIn("history", body)

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

    def test_get_single_microorganism_history(self):
        microorganism = MicroorganismFactory.create()
        response = self.client.get(
            f"{reverse('api:single_microorganism', kwargs={'pk': microorganism.id})}?history=true"
        )
        body = response.json()

        self.assertIn("history", body)

        response = self.client.get(reverse("api:single_microorganism", kwargs={"pk": microorganism.id}))
        body = response.json()

        self.assertNotIn("history", body)

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

    def test_get_single_substance_history(self):
        substance = SubstanceFactory.create()
        response = self.client.get(f"{reverse('api:single_substance', kwargs={'pk': substance.id})}?history=true")
        body = response.json()

        self.assertIn("history", body)

        response = self.client.get(reverse("api:single_substance", kwargs={"pk": substance.id}))
        body = response.json()

        self.assertNotIn("history", body)

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


class TestElementsCreateApi(APITestCase):
    @authenticate
    def test_create_single_plant(self):
        """
        Une instructrice peut créer une nouvelle plante avec des synonymes
        """
        InstructionRoleFactory(user=authenticate.user)

        family = PlantFamilyFactory.create()
        part_1 = PlantPartFactory.create()
        part_2 = PlantPartFactory.create()
        substance = SubstanceFactory.create()
        self.assertEqual(Plant.objects.count(), 0)
        payload = {
            "caName": "My new plant",
            "caFamily": family.id,
            "caStatus": IngredientStatus.AUTHORIZED,
            "synonyms": [
                {"name": "A latin name"},
                {"name": "A latin name"},
                {"name": "A second one"},
                {"name": "My new plant"},
            ],
            "plantParts": [part_1.id, part_2.id],
            "substances": [substance.id],
            "caPublicComments": "Test",
            "caPrivateComments": "Test private",
            "novelFood": True,
        }
        response = self.client.post(reverse("api:plant_list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()

        self.assertIn("id", body)
        plant = Plant.objects.get(id=body["id"])
        self.assertEqual(plant.name, "My new plant")
        self.assertEqual(plant.family, family)
        self.assertEqual(plant.plantsynonym_set.count(), 2)  # deduplication of synonym
        self.assertTrue(plant.plantsynonym_set.filter(name="A latin name").exists())
        self.assertTrue(plant.plantsynonym_set.filter(name="A second one").exists())
        self.assertEqual(plant.plant_parts.count(), 2)
        self.assertEqual(plant.substances.count(), 1)
        self.assertEqual(plant.public_comments, "Test")
        self.assertEqual(plant.private_comments, "Test private")
        self.assertEqual(plant.status, IngredientStatus.AUTHORIZED)
        self.assertTrue(plant.novel_food)

    @authenticate
    def test_cannot_create_single_plant_not_authorized(self):
        payload = {"caName": "My new plant"}
        response = self.client.post(reverse("api:plant_list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_single_microorganism(self):
        """
        Une instructrice peut créer un nouveau microorganisme avec des synonymes
        """
        InstructionRoleFactory(user=authenticate.user)

        substance = SubstanceFactory.create()
        self.assertEqual(Microorganism.objects.count(), 0)
        payload = {
            "caGenus": "My new microorganism",
            "caSpecies": "A species",
            "caStatus": IngredientStatus.AUTHORIZED,  # TODO: est-ce qu'on a besoin de soutenir les quatre valeurs ?
            "synonyms": [
                {"name": "A latin name"},
                {"name": "A second one"},
            ],
            "substances": [substance.id],
            "caPublicComments": "Test",
            "caPrivateComments": "Test private",
        }
        response = self.client.post(reverse("api:microorganism_list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()

        self.assertIn("id", body)
        microorganism = Microorganism.objects.get(id=body["id"])
        self.assertEqual(microorganism.genus, "My new microorganism")
        self.assertEqual(microorganism.species, "A species")
        self.assertEqual(microorganism.microorganismsynonym_set.count(), 2)  # deduplication of synonym
        self.assertTrue(microorganism.microorganismsynonym_set.filter(name="A latin name").exists())
        self.assertTrue(microorganism.microorganismsynonym_set.filter(name="A second one").exists())
        self.assertEqual(microorganism.substances.count(), 1)
        self.assertEqual(microorganism.public_comments, "Test")
        self.assertEqual(microorganism.private_comments, "Test private")
        self.assertEqual(microorganism.status, IngredientStatus.AUTHORIZED)

    @authenticate
    def test_cannot_create_single_microorganism_not_authorized(self):
        payload = {"caName": "My new microorganism"}
        response = self.client.post(reverse("api:microorganism_list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
