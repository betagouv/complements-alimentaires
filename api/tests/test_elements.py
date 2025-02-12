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
    SubstanceUnitFactory,
    PlantSynonymFactory,
)
from data.models import IngredientType, Plant, IngredientStatus, Microorganism, Substance, Ingredient
from data.choices import IngredientActivity

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

    def test_get_ingredient_returns_generated_fields(self):
        """
        L'endpoint utilisé pour modifier un ingrédient devrait rendre les données des champs générés
        et non pas que le champ ca_X
        J'ajoute un test en supposant qu'on réutilise la même logique entre les 4 types.
        """
        plant = PlantFactory.create(ca_name="", siccrf_name="SICCRF name")
        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["name"], "SICCRF name")


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
            "name": "My new plant",
            "family": family.id,
            "status": IngredientStatus.AUTHORIZED,
            "synonyms": [
                {"name": "A latin name"},
                {"name": "A latin name"},
                {"name": "A second one"},
                {"name": "My new plant"},
            ],
            "plantParts": [part_1.id, part_2.id],
            "substances": [substance.id],
            "publicComments": "Test",
            "privateComments": "Test private",
            "novelFood": True,
        }
        response = self.client.post(reverse("api:plant_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()

        self.assertIn("id", body)
        plant = Plant.objects.get(id=body["id"])
        self.assertEqual(plant.ca_name, "My new plant")
        self.assertEqual(plant.ca_family, family)
        self.assertEqual(plant.plantsynonym_set.count(), 2)  # deduplication of synonym
        self.assertTrue(plant.plantsynonym_set.filter(name="A latin name").exists())
        self.assertTrue(plant.plantsynonym_set.filter(name="A second one").exists())
        self.assertEqual(plant.plant_parts.count(), 2)
        self.assertEqual(plant.substances.count(), 1)
        self.assertEqual(plant.ca_public_comments, "Test")
        self.assertEqual(plant.ca_private_comments, "Test private")
        self.assertEqual(plant.ca_status, IngredientStatus.AUTHORIZED)
        self.assertTrue(plant.novel_food)

    @authenticate
    def test_cannot_create_single_plant_not_authorized(self):
        payload = {"name": "My new plant"}
        response = self.client.post(reverse("api:plant_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_single_microorganism(self):
        """
        Une instructrice peut créer un nouveau microorganisme avec des synonymes
        """
        InstructionRoleFactory(user=authenticate.user)

        self.assertEqual(Microorganism.objects.count(), 0)
        payload = {
            "genus": "My new microorganism",
            "species": "A species",
            "status": IngredientStatus.AUTHORIZED,
            "synonyms": [
                {"name": "A latin name"},
                {"name": "A second one"},
            ],
            "publicComments": "Test",
            "privateComments": "Test private",
            "novelFood": True,
        }
        response = self.client.post(reverse("api:microorganism_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()

        self.assertIn("id", body)
        microorganism = Microorganism.objects.get(id=body["id"])
        self.assertEqual(microorganism.ca_genus, "My new microorganism")
        self.assertEqual(microorganism.ca_species, "A species")
        self.assertEqual(microorganism.microorganismsynonym_set.count(), 2)  # deduplication of synonym
        self.assertTrue(microorganism.microorganismsynonym_set.filter(name="A latin name").exists())
        self.assertTrue(microorganism.microorganismsynonym_set.filter(name="A second one").exists())
        self.assertEqual(microorganism.substances.count(), 0)
        self.assertEqual(microorganism.ca_public_comments, "Test")
        self.assertEqual(microorganism.ca_private_comments, "Test private")
        self.assertEqual(microorganism.ca_status, IngredientStatus.AUTHORIZED)
        self.assertTrue(microorganism.novel_food)

    @authenticate
    def test_cannot_create_single_microorganism_not_authorized(self):
        payload = {"name": "My new microorganism"}
        response = self.client.post(reverse("api:microorganism_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_single_substance(self):
        """
        Une instructrice peut créer une nouvelle substance avec des synonymes
        """
        InstructionRoleFactory(user=authenticate.user)

        unit = SubstanceUnitFactory.create()
        self.assertEqual(Substance.objects.count(), 0)
        payload = {
            "name": "My new substance",
            "status": IngredientStatus.AUTHORIZED,
            "casNumber": "1234",
            "einecNumber": "5678",
            "maxQuantity": 3.4,
            "nutritionalReference": 1.2,
            "unit": unit.id,
        }
        response = self.client.post(reverse("api:substance_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()

        self.assertIn("id", body)
        substance = Substance.objects.get(id=body["id"])
        self.assertEqual(substance.ca_name, "My new substance")
        self.assertEqual(substance.ca_status, IngredientStatus.AUTHORIZED)
        self.assertEqual(substance.ca_cas_number, "1234")
        self.assertEqual(substance.ca_einec_number, "5678")
        self.assertEqual(substance.ca_max_quantity, 3.4)
        self.assertEqual(substance.ca_nutritional_reference, 1.2)
        self.assertEqual(substance.unit, unit)

    @authenticate
    def test_cannot_create_single_substance_not_authorized(self):
        payload = {"name": "My new substance"}
        response = self.client.post(reverse("api:substance_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_single_ingredient(self):
        """
        Une instructrice peut créer un nouvel ingredient avec des synonymes
        """
        InstructionRoleFactory(user=authenticate.user)

        substance = SubstanceFactory.create()
        self.assertEqual(Ingredient.objects.count(), 0)
        payload = {
            "name": "My new ingredient",
            "status": IngredientStatus.AUTHORIZED,
            "ingredientType": 4,
            "substances": [substance.id],
        }
        response = self.client.post(reverse("api:ingredient_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()

        self.assertIn("id", body)
        ingredient = Ingredient.objects.get(id=body["id"])
        self.assertEqual(ingredient.ca_name, "My new ingredient")
        self.assertEqual(ingredient.ca_status, IngredientStatus.AUTHORIZED)
        self.assertEqual(ingredient.ingredient_type, IngredientType.ACTIVE_INGREDIENT)
        self.assertEqual(ingredient.activity, IngredientActivity.ACTIVE)
        self.assertEqual(ingredient.substances.count(), 1)

    @authenticate
    def test_cannot_create_single_ingredient_not_authorized(self):
        payload = {"name": "My new ingredient"}
        response = self.client.post(reverse("api:ingredient_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestElementsModifyApi(APITestCase):
    # def test_cannot_modify_ingredient_not_authenticated(self):
    #     substance = SubstanceFactory.create(siccrf_name="original name")
    #     response = self.client.patch(reverse("api:single_substance", kwargs={"pk": substance.id}), {"name": "test"}, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(substance.name, "original name")

    # @authenticate
    # def test_cannot_modify_ingredient_not_instructor(self):
    #     substance = SubstanceFactory.create(siccrf_name="original name")
    #     response = self.client.patch(reverse("api:single_substance", kwargs={"pk": substance.id}), {"name": "test"}, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(substance.name, "original name")

    @authenticate
    def test_can_modify_ingredient_ca_fields(self):
        """
        Les instructrices peuvent modifier un ingrédient, et un mapping est fait entre le nom du champ sans prefix -> ca_
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create(
            siccrf_name="original name", ca_name="", unit=SubstanceUnitFactory.create()
        )
        new_unit = SubstanceUnitFactory.create()
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {"name": "test", "unit": new_unit.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        self.assertEqual(substance.siccrf_name, "original name")
        self.assertEqual(substance.ca_name, "test")
        self.assertEqual(substance.unit, new_unit, "Les champs sans ca_ équivelant sont aussi sauvegardés")

    @authenticate
    def test_can_modify_add_delete_synonyms(self):
        """
        En passant tous les synonyms c'est possible de MAJ les synonymes
        """
        InstructionRoleFactory(user=authenticate.user)
        plant = PlantFactory.create()
        PlantSynonymFactory.create(name="Old name", standard_name=plant)
        synonym_2 = PlantSynonymFactory.create(name="Don't change", standard_name=plant)
        synonym_to_delete = PlantSynonymFactory.create(standard_name=plant)

        response = self.client.patch(
            reverse("api:single_plant", kwargs={"pk": plant.id}),
            {"synonyms": [{"name": "New synonyme"}, {"name": "New name"}, {"name": synonym_2.name}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plant.refresh_from_db()
        self.assertEqual(plant.plantsynonym_set.count(), 3)
        self.assertTrue(plant.plantsynonym_set.filter(name="New synonyme").exists())
        self.assertTrue(plant.plantsynonym_set.filter(name="New name").exists())
        self.assertTrue(plant.plantsynonym_set.filter(name="Don't change").exists())
        self.assertFalse(plant.plantsynonym_set.filter(name=synonym_to_delete.name).exists())
        # TODO: how to handle invalid ids?
        # TODO: how to handle ids not attached to this ingredient?
        # TODO: what about modifying to then match an existing synonym?
        # TODO: what about invalid synonym format?
        # -> atomicise transaction

    # TODO: modify synonymes
    # TODO: modify substances
    # TODO: delete by marking as obsolete
