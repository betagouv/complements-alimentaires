from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.choices import IngredientActivity
from data.factories import (
    ComputedSubstanceFactory,
    DeclaredSubstanceFactory,
    IngredientFactory,
    InstructionRoleFactory,
    MaxQuantityPerPopulationRelationFactory,
    MicroorganismFactory,
    OngoingInstructionDeclarationFactory,
    PlantFactory,
    PlantFamilyFactory,
    PlantPartFactory,
    PlantSynonymFactory,
    PopulationFactory,
    SubstanceFactory,
    SubstanceSynonymFactory,
    SubstanceUnitFactory,
)
from data.models import Ingredient, IngredientStatus, IngredientType, Microorganism, Part, Plant, Population
from data.models.substance import MaxQuantityPerPopulationRelation, Substance

from .utils import authenticate


class TestElementsFetchApi(APITestCase):
    def test_get_single_plant(self):
        plant = PlantFactory.create()
        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(plant.name, body["name"])
        self.assertEqual(plant.id, body["id"])

    def test_get_single_plant_history_unauthenticated(self):
        plant = PlantFactory.create()
        response = self.client.get(f"{reverse('api:single_plant', kwargs={'pk': plant.id})}?history=true")
        body = response.json()

        self.assertIn("history", body)
        self.assertIn("changedFields", body["history"][0])
        self.assertIn("historyType", body["history"][0])
        self.assertIn("historyDate", body["history"][0])
        self.assertNotIn("user", body["history"][0])
        self.assertNotIn("historyChangeReason", body["history"][0])

        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        body = response.json()

        self.assertNotIn("history", body)

    @authenticate
    def test_get_single_plant_history_instructor(self):
        plant = PlantFactory.create()
        plant.name = "Test change"
        plant.save()
        self.assertEqual(plant.name, "Test change")
        InstructionRoleFactory(user=authenticate.user)
        response = self.client.get(f"{reverse('api:single_plant', kwargs={'pk': plant.id})}?history=true")
        body = response.json()

        self.assertIn("user", body["history"][0])
        self.assertEqual(body["history"][0]["changedFields"], ["nom CA"])
        self.assertIn("historyType", body["history"][0])
        self.assertIn("historyDate", body["history"][0])
        self.assertIn("user", body["history"][0])
        self.assertIn("historyChangeReason", body["history"][0])

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
        plant = PlantFactory.create(name="SICCRF name")
        response = self.client.get(reverse("api:single_plant", kwargs={"pk": plant.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["name"], "SICCRF name")


class TestElementsCreateApi(APITestCase):
    def setUp(self):
        self.general_pop = PopulationFactory.create(name="Population générale")

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
            "plantParts": [{"plantpart": part_1.id, "isUseful": True}, {"plantpart": part_2.id, "isUseful": False}],
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
        self.assertEqual(plant.name, "My new plant")
        self.assertEqual(plant.family, family)
        self.assertEqual(plant.plantsynonym_set.count(), 2)  # deduplication of synonym
        self.assertTrue(plant.plantsynonym_set.filter(name="A latin name").exists())
        self.assertTrue(plant.plantsynonym_set.filter(name="A second one").exists())
        self.assertEqual(plant.part_set.count(), 2)
        self.assertTrue(plant.part_set.get(plantpart=part_1.id).is_useful)
        self.assertFalse(plant.part_set.get(plantpart=part_2.id).is_useful)
        self.assertEqual(plant.substances.count(), 1)
        self.assertEqual(plant.public_comments, "Test")
        self.assertEqual(plant.private_comments, "Test private")
        self.assertEqual(plant.status, IngredientStatus.AUTHORIZED)
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
        self.assertEqual(microorganism.genus, "My new microorganism")
        self.assertEqual(microorganism.species, "A species")
        self.assertEqual(microorganism.microorganismsynonym_set.count(), 2)  # deduplication of synonym
        self.assertTrue(microorganism.microorganismsynonym_set.filter(name="A latin name").exists())
        self.assertTrue(microorganism.microorganismsynonym_set.filter(name="A second one").exists())
        self.assertEqual(microorganism.substances.count(), 0)
        self.assertEqual(microorganism.public_comments, "Test")
        self.assertEqual(microorganism.private_comments, "Test private")
        self.assertEqual(microorganism.status, IngredientStatus.AUTHORIZED)
        self.assertTrue(microorganism.novel_food)

    @authenticate
    def test_cannot_create_single_microorganism_not_authorized(self):
        payload = {"name": "My new microorganism"}
        response = self.client.post(reverse("api:microorganism_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_single_substance(self):
        """
        Une instructrice peut créer une nouvelle substance avec des synonymes et plusieurs quantités maximales
        """
        InstructionRoleFactory(user=authenticate.user)
        other_pop = PopulationFactory(name="Autre population")

        unit = SubstanceUnitFactory.create()
        self.assertEqual(Substance.objects.count(), 0)
        payload = {
            "name": "My new substance",
            "status": IngredientStatus.AUTHORIZED,
            "casNumber": "1234",
            "einecNumber": "5678",
            "maxQuantities": [
                {"population": self.general_pop.id, "maxQuantity": 3.4},
                {"population": other_pop.id, "maxQuantity": 4.5},
            ],
            "nutritionalReference": 1.2,
            "unit": unit.id,
        }
        response = self.client.post(reverse("api:substance_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()

        self.assertIn("id", body)
        substance = Substance.objects.get(id=body["id"])
        self.assertEqual(substance.name, "My new substance")
        self.assertEqual(substance.status, IngredientStatus.AUTHORIZED)
        self.assertEqual(substance.cas_number, "1234")
        self.assertEqual(substance.einec_number, "5678")
        self.assertEqual(substance.max_quantity, 3.4)
        self.assertEqual(
            substance.maxquantityperpopulationrelation_set.get(
                population=Population.objects.get(name="Population générale")
            ).max_quantity,
            3.4,
        )
        self.assertEqual(
            substance.maxquantityperpopulationrelation_set.get(
                population=Population.objects.get(name="Autre population")
            ).max_quantity,
            4.5,
        )
        self.assertEqual(substance.nutritional_reference, 1.2)
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
        self.assertEqual(ingredient.name, "My new ingredient")
        self.assertEqual(ingredient.status, IngredientStatus.AUTHORIZED)
        self.assertEqual(ingredient.ingredient_type, IngredientType.ACTIVE_INGREDIENT)
        self.assertEqual(ingredient.activity, IngredientActivity.ACTIVE)
        self.assertEqual(ingredient.substances.count(), 1)

    @authenticate
    def test_cannot_create_single_ingredient_not_authorized(self):
        payload = {"name": "My new ingredient"}
        response = self.client.post(reverse("api:ingredient_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_change_reason_on_create_ingredient(self):
        """
        Une raison de changement est donnée quand une création est effectué depuis cet API
        """
        InstructionRoleFactory(user=authenticate.user)

        payload = {"name": "My new ingredient", "changeReason": "Création test"}
        response = self.client.post(reverse("api:ingredient_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        ingredient = Ingredient.objects.get(name="My new ingredient")
        self.assertEqual(ingredient.history.first().history_change_reason, "Création test")


class TestElementsModifyApi(APITestCase):
    def setUp(self):
        self.general_pop = PopulationFactory.create(name="Population générale")

    def test_cannot_modify_ingredient_not_authenticated(self):
        substance = SubstanceFactory.create(name="")
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}), {"name": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(substance.name, "original name")

    @authenticate
    def test_cannot_modify_ingredient_not_instructor(self):
        substance = SubstanceFactory.create(name="")
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}), {"name": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(substance.name, "original name")

    @authenticate
    def test_can_modify_ingredient_ca_fields(self):
        """
        Les instructrices peuvent modifier un ingrédient, et un mapping est fait entre le nom du champ sans prefix -> ca_
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create(
            name="original name",
            unit=SubstanceUnitFactory.create(),
            status=IngredientStatus.AUTHORIZED,
            must_specify_quantity=True,
        )
        MaxQuantityPerPopulationRelationFactory(
            substance=substance,
            population=self.general_pop,
            max_quantity=3.4,
        )

        new_unit = SubstanceUnitFactory.create()
        self.assertEqual(
            substance.max_quantity, 3.4, "La quantité max pour la population générale est la bonne avant modification"
        )
        self.assertTrue(substance.must_specify_quantity, "Le champ siccrf est vrai, comme donné dans le factory")
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "name": "test",
                "unit": new_unit.id,
                "maxQuantities": [{"population": self.general_pop.id, "maxQuantity": 35}],
                "status": IngredientStatus.NO_STATUS,
                "mustSpecifyQuantity": False,
                "changeReason": "Test change",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        self.assertEqual(substance.siccrfname, "original name")
        self.assertEqual(substance.name, "test")
        self.assertEqual(substance.unit, new_unit, "Les champs sans ca_ équivelant sont aussi sauvegardés")
        self.assertEqual(
            substance.max_quantity, 35, "La quantité max pour la population générale est aussi sauvegardée"
        )
        self.assertEqual(
            substance.status, IngredientStatus.NO_STATUS, "C'est possible de remettre la valeur originelle"
        )
        self.assertTrue(substance.must_specify_quantity, "Le champ siccrf n'est pas changé")
        self.assertEqual(
            substance.history.first().history_change_reason,
            "Test change",
            "Le message en texte libre est sauvegardée comme raison de changement",
        )

    @authenticate
    def test_can_give_public_change_reason(self):
        """
        Ainsi qu'une raison de changement privé, c'est possible de donner une raison de visibilité publique
        """
        InstructionRoleFactory(user=authenticate.user)
        ingredient = IngredientFactory.create()

        payload = {"name": "Nouvel nom", "changeReason": "Raison privée", "publicChangeReason": "Raison publique"}
        response = self.client.patch(
            reverse("api:single_ingredient", kwargs={"pk": ingredient.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ingredient.refresh_from_db()
        self.assertEqual(ingredient.history.first().history_change_reason, "Raison privée")
        self.assertEqual(ingredient.history.first().history_public_change_reason, "Raison publique")

    @authenticate
    def test_can_modify_substance_max_quantities(self):
        """
        Les instructrices peuvent rajouter une doses max pour la population générale en ajoutant
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create(
            name="original name",
            unit=SubstanceUnitFactory.create(),
            status=IngredientStatus.AUTHORIZED,
        )
        self.assertEqual(
            substance.max_quantity, None, "La quantité max pour la population générale n'est pas encore définie"
        )
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "maxQuantities": [{"population": self.general_pop.id, "maxQuantity": 666}],
                "changeReason": "Add first pop",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        self.assertEqual(substance.max_quantity, 666, "La quantité max pour la population générale est créée")
        self.assertTrue(
            MaxQuantityPerPopulationRelation.objects.filter(substance=substance, population=self.general_pop).exists()
        )
        other_pop = PopulationFactory.create(name="pop non-autorisée")
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "maxQuantities": [
                    {"population": self.general_pop.id, "maxQuantity": 666},
                    {"population": other_pop.id, "maxQuantity": 0},
                ],
                "changeReason": "Add second pop",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        self.assertEqual(
            MaxQuantityPerPopulationRelation.objects.get(
                substance=substance, population=self.general_pop
            ).max_quantity,
            666,
            "La dose max pour la pop générale n'a pas été modifiée",
        )
        self.assertEqual(
            MaxQuantityPerPopulationRelation.objects.get(
                substance=substance, population=Population.objects.get(name="pop non-autorisée")
            ).max_quantity,
            0,
            "Une restriction d'usage pour une pop a été créé",
        )

        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "maxQuantities": [{"population": other_pop.id, "maxQuantity": 45}],
                "changeReason": "Add second pop",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        self.assertFalse(
            MaxQuantityPerPopulationRelation.objects.filter(substance=substance, population=self.general_pop).exists(),
            "La dose max pour la pop générale a été supprimée",
        )
        self.assertEqual(
            MaxQuantityPerPopulationRelation.objects.get(substance=substance, population=other_pop).max_quantity,
            45,
            "La dose max pour l'autre population a été modifiée",
        )

    @authenticate
    def test_can_modify_substance_without_modifying_max_quantity(self):
        """
        Les instructrices peuvent modifier un champ sans que la dose max se trouve supprimée
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create(
            name="original name",
            unit=SubstanceUnitFactory.create(),
            status=IngredientStatus.AUTHORIZED,
        )
        MaxQuantityPerPopulationRelationFactory(substance=substance, population=self.general_pop, max_quantity=24)
        new_unit = SubstanceUnitFactory.create()
        self.assertEqual(substance.max_quantity, 24, "La quantité max pour la population générale est définie")
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "name": "test",
                "unit": new_unit.id,
                "status": IngredientStatus.NO_STATUS,
                "changeReason": "Test change",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        self.assertEqual(substance.max_quantity, 24, "La quantité max pour la population générale n'est pas modifiée")
        self.assertTrue(
            MaxQuantityPerPopulationRelation.objects.filter(substance=substance, population=self.general_pop).exists()
        )

    @authenticate
    def test_can_modify_plant_parts(self):
        """
        Les instructrices peuvent modifier les parties de plantes autorisées et non-autorisées
        """
        InstructionRoleFactory(user=authenticate.user)

        old_part = PlantPartFactory.create()
        questionable_part = PlantPartFactory.create()
        new_dangerous_part = PlantPartFactory.create()
        plant = PlantFactory.create()
        Part.objects.create(plant=plant, plantpart=old_part, is_useful=True)
        Part.objects.create(plant=plant, plantpart=questionable_part, is_useful=False)

        self.assertTrue(plant.part_set.get(plantpart=old_part.id).is_useful)
        self.assertFalse(plant.part_set.get(plantpart=questionable_part.id).is_useful)
        self.assertFalse(plant.part_set.filter(plantpart=new_dangerous_part.id).exists())

        payload = {
            "plantParts": [
                {"plantpart": questionable_part.id, "isUseful": True},
                {"plantpart": new_dangerous_part.id, "isUseful": False},
            ],
        }
        response = self.client.patch(reverse("api:single_plant", kwargs={"pk": plant.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plant.refresh_from_db()
        self.assertFalse(plant.part_set.filter(plantpart=old_part.id).exists())
        self.assertTrue(plant.part_set.get(plantpart=questionable_part.id).is_useful)
        self.assertFalse(plant.part_set.get(plantpart=new_dangerous_part.id).is_useful)

    @authenticate
    def test_cannot_give_same_part_twice(self):
        """
        Si la même partie est donnée en autorisée et non-autorisée, donne un 400
        """
        InstructionRoleFactory(user=authenticate.user)

        duplicate_part = PlantPartFactory.create()
        other_part = PlantPartFactory.create()
        plant = PlantFactory.create()

        self.assertFalse(plant.part_set.filter(plantpart=duplicate_part.id).exists())
        self.assertFalse(plant.part_set.filter(plantpart=other_part.id).exists())

        payload = {
            "name": "new name",
            "plantParts": [
                {"plantpart": other_part.id, "isUseful": True},
                {"plantpart": duplicate_part.id, "isUseful": True},
                {"plantpart": duplicate_part.id, "isUseful": False},
            ],
        }
        response = self.client.patch(reverse("api:single_plant", kwargs={"pk": plant.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        plant.refresh_from_db()
        self.assertFalse(
            plant.part_set.filter(plantpart=duplicate_part.id).exists(),
            "la partie en doublon ne devrait pas été ajoutée à la plante",
        )
        self.assertFalse(
            plant.part_set.filter(plantpart=other_part.id).exists(),
            "l'autre partie ne devrait pas été ajoutée à la plante",
        )
        self.assertNotEqual(plant.name, "new name", "autres modifications devraient être ignorées aussi")

    @authenticate
    def test_update_siccrf_max_quantity(self):
        """
        Si une dose max est specifiée avec les données siccrf, quand on fait la modif ça ajoute dans le champ equivalent ca_
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create(
            name="original name",
            unit=SubstanceUnitFactory.create(),
        )
        MaxQuantityPerPopulationRelationFactory(substance=substance, population=self.general_pop, max_quantity=24)
        self.assertEqual(substance.max_quantity, 24, "La quantité max pour la population générale est définie")
        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "maxQuantities": [
                    {"population": self.general_pop.id, "maxQuantity": 666},
                ],
                "changeReason": "Add second pop",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        general_pop_max = MaxQuantityPerPopulationRelation.objects.get(
            substance=substance, population=self.general_pop
        )
        self.assertEqual(
            general_pop_max.max_quantity,
            666,
            "La dose max pour la pop générale est MAJ",
        )

    @authenticate
    def test_max_quantities_errors(self):
        """
        Voir si on envoie des bonnes erreurs quand les données de quantités max sont mauvaises
        Ça test que la MAJ, mais on devrait avoir les mêmes règles sur la création
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create(name="original name")

        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "maxQuantities": [
                    {"population": self.general_pop.id, "maxQuantity": 1},
                    {"population": self.general_pop.id, "maxQuantity": 12},
                ],
                "changeReason": "duplicate population",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["fieldErrors"]["maxQuantities"][0],
            "Veuillez donner qu'une quantité maximale par population",
        )

        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {
                "maxQuantities": [
                    {"population": 999, "maxQuantity": 1},
                ],
                "changeReason": "bad pop id test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_delete_data(self):
        """
        C'est possible de supprimer des données optionnelles en passant un string vide
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create(
            public_comments="CA comment",
            private_comments="private comment",
            cas_number="CA number",
        )
        MaxQuantityPerPopulationRelationFactory(
            substance=substance,
            population=self.general_pop,
            max_quantity=3.4,
        )

        SubstanceSynonymFactory.create(name="To delete", standard_name=substance)

        response = self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {"public_comments": "", "private_comments": "", "cas_number": "", "max_quantities": [], "synonyms": []},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        substance.refresh_from_db()
        self.assertEqual(substance.public_comments, "")
        self.assertEqual(substance.private_comments, "")
        self.assertEqual(substance.cas_number, "")

        self.assertFalse(
            substance.maxquantityperpopulationrelation_set.filter(population__name="Population générale").exists()
        )
        self.assertIsNone(substance.max_quantity)
        self.assertEqual(substance.substancesynonym_set.count(), 0)

    @authenticate
    def test_deduplicate_siccrf_data(self):
        """
        Si la valeur passée est égale à la valeur dans un champ siccrf_
        la valeur n'est pas copiée dans le champ ca_
        """
        InstructionRoleFactory(user=authenticate.user)
        microorganism = MicroorganismFactory.create(genus="siccrf genus")
        response = self.client.patch(
            reverse("api:single_microorganism", kwargs={"pk": microorganism.id}),
            {"genus": "siccrf genus"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        microorganism.refresh_from_db()
        self.assertEqual(microorganism.genus, "siccrf genus")

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
            {
                "synonyms": [
                    {"name": "New synonyme"},
                    {"name": "New name"},
                    {"name": synonym_2.name},
                    {"name": synonym_2.name},
                ]
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plant.refresh_from_db()
        self.assertEqual(plant.plantsynonym_set.count(), 3)
        self.assertTrue(plant.plantsynonym_set.filter(name="New synonyme").exists())
        self.assertTrue(plant.plantsynonym_set.filter(name="New name").exists())
        self.assertTrue(plant.plantsynonym_set.filter(name="Don't change").exists())
        self.assertFalse(plant.plantsynonym_set.filter(name=synonym_to_delete.name).exists())

    @authenticate
    def test_atomic_transaction_synonym_fail(self):
        """
        Si la MAJ de synonymes échoue, ignore toutes les modifs
        """
        InstructionRoleFactory(user=authenticate.user)
        plant = PlantFactory.create()
        PlantSynonymFactory.create(name="a plant", standard_name=plant)
        self.client.patch(
            reverse("api:single_plant", kwargs={"pk": plant.id}),
            {"name": "New name", "synonyms": [{"name": "New synonym"}, {"test": "bad format"}]},
            format="json",
        )
        plant.refresh_from_db()
        self.assertNotEqual(plant.name, "New name")
        self.assertEqual(plant.plantsynonym_set.count(), 1)
        self.assertTrue(plant.plantsynonym_set.filter(name="a plant").exists())

    @authenticate
    def test_can_modify_add_delete_substances(self):
        """
        C'est possible de modifier la liste de substances associées à l'ingrédient
        """
        InstructionRoleFactory(user=authenticate.user)
        substance = SubstanceFactory.create()
        substance_to_delete = SubstanceFactory.create()
        new_substance = SubstanceFactory.create()

        microorganism = MicroorganismFactory.create(substances=[substance, substance_to_delete])

        response = self.client.patch(
            reverse("api:single_microorganism", kwargs={"pk": microorganism.id}),
            {"substances": [substance.id, new_substance.id]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        microorganism.refresh_from_db()
        self.assertEqual(microorganism.substances.count(), 2)
        self.assertTrue(microorganism.substances.filter(id=substance.id).exists())
        self.assertTrue(microorganism.substances.filter(id=new_substance.id).exists())
        self.assertFalse(microorganism.substances.filter(id=substance_to_delete.id).exists())

    @authenticate
    @patch("config.tasks.recalculate_article_for_ongoing_declarations")
    def test_article_recalculation_triggered(self, mocked_task):
        """
        Si une modif pourrait modifier l'article calculé d'une déclaration, la tâche pour recalculer les déclarations
        en masse devrait être appelée
        """
        InstructionRoleFactory(user=authenticate.user)

        microorganism = MicroorganismFactory.create()

        self.client.patch(
            reverse("api:single_microorganism", kwargs={"pk": microorganism.id}),
            {"substances": []},
            format="json",
        )

        mocked_task.assert_called_once()

    @authenticate
    @patch("config.tasks.recalculate_article_for_ongoing_declarations")
    def test_article_recalculation_triggered_with_computed_and_declared_substance_declarations(self, mocked_task):
        """
        Si il y a un changement de substance, la tâche doit être appelé avec toutes les déclarations qui utilisent
        la substance, si c'est de manière déclarée ou calculée
        """
        InstructionRoleFactory(user=authenticate.user)

        declared_substance_declaration = OngoingInstructionDeclarationFactory.create()
        computed_substance_declaration = OngoingInstructionDeclarationFactory.create()
        substance = SubstanceFactory.create(status=IngredientStatus.AUTHORIZED)

        DeclaredSubstanceFactory.create(substance=substance, declaration=declared_substance_declaration)
        ComputedSubstanceFactory.create(substance=substance, declaration=computed_substance_declaration)

        self.assertTrue(declared_substance_declaration.declared_substances.filter(substance=substance).exists())
        self.assertTrue(computed_substance_declaration.computed_substances.filter(substance=substance).exists())

        self.client.patch(
            reverse("api:single_substance", kwargs={"pk": substance.id}),
            {"status": IngredientStatus.NOT_AUTHORIZED},
            format="json",
        )

        # Les déclarations avec des substances calculées ainsi que les substances déclarées sont MAJ
        mocked_task.assert_called_once()
        arguments = mocked_task.call_args.args
        queryset_argument = arguments[0]
        self.assertEqual(queryset_argument.count(), 2)
        self.assertTrue(queryset_argument.filter(id=declared_substance_declaration.id).exists())
        self.assertTrue(queryset_argument.filter(id=computed_substance_declaration.id).exists())

    @authenticate
    @patch("config.tasks.recalculate_article_for_ongoing_declarations")
    def test_article_recalculation_not_triggered_boring_fields(self, mocked_task):
        """
        Si une modif est effectuée que sur des champs "safe", n'appelle pas la tâche
        On fait la vérif sur les champs "safe" parce que c'est moins un pb si l'article est recalculé sans avoir besoin
        que si ce n'est pas recalculé quand il y a besoin
        """
        InstructionRoleFactory(user=authenticate.user)

        microorganism = MicroorganismFactory.create()

        self.client.patch(
            reverse("api:single_microorganism", kwargs={"pk": microorganism.id}),
            {
                "genus": "test",
                "species": "test",
                "synonymes": [],
                "public_comments": "",
                "private_comments": "",
                "novel_food": False,
                "change_reason": "",
                "public_change_reason": "",
            },
            format="json",
        )

        mocked_task.assert_not_called()
