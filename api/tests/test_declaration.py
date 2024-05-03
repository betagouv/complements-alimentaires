import base64
import os

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.choices import AuthorizationModes, CountryChoices, FrAuthorizationReasons
from data.factories import (
    CompanyFactory,
    ConditionFactory,
    DeclarantRoleFactory,
    DeclarationFactory,
    EffectFactory,
    GalenicFormulationFactory,
    IngredientFactory,
    InstructionReadyDeclarationFactory,
    InstructionRoleFactory,
    MicroorganismFactory,
    PlantFactory,
    PlantPartFactory,
    PopulationFactory,
    SubstanceFactory,
    SubstanceUnitFactory,
)
from data.models import Attachment, Declaration

from .utils import authenticate


class TestDeclarationApi(APITestCase):
    @authenticate
    def test_create_not_allowed_without_role(self):
        """
        La création des déclaration est possible seulement pour les users avec
        rôle « declarant »
        """
        payload = {
            "company": CompanyFactory().id,
            "name": "name",
        }
        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_wrong_company_declaration(self):
        DeclarantRoleFactory(user=authenticate.user)
        wrong_company = CompanyFactory()
        payload = {
            "company": wrong_company.id,
            "name": "name",
        }
        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_declaration_product_data(self):
        """
        Création de l'objet « déclaration » avec les données du produit
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        conditions = [ConditionFactory() for _ in range(3)]
        effect1 = EffectFactory(ca_name="Artères et cholestérol")
        effect2 = EffectFactory(ca_name="Autre (à préciser)")
        populations = [PopulationFactory() for _ in range(3)]
        unit = SubstanceUnitFactory()
        galenic_formulation = GalenicFormulationFactory()

        payload = {
            "company": company.id,
            "address": "243 rue Victor Hugo",
            "additional_details": "Deuxième étage",
            "postalCode": "69004",
            "city": "Lyon",
            "cedex": "Lyon 4",
            "country": "FR",
            "effects": [effect1.id, effect2.id],
            "otherEffects": "Moduler les défenses naturelles",
            "conditionsNotRecommended": [conditions[0].id, conditions[1].id],
            "populations": [populations[0].id, populations[1].id],
            "name": "Extrait de Chaga BIO",
            "brand": "Azona Rome",
            "gamme": "Vegan",
            "flavor": "Myrtille",
            "description": "Ce complément alimentaire naturel est composé d'un extrait de Chaga BIO concentré à 30% polysaccharides hautement dosé pour une efficacité optimale",
            "galenicFormulation": galenic_formulation.id,
            "unitQuantity": "500",
            "unitMeasurement": unit.id,
            "conditioning": "Sans chitine, pour une bonne absorption et tolérance digestive",
            "dailyRecommendedDose": "2",
            "minimumDuration": "1 mois",
            "instructions": "Prendre 1 à 2 gélules par jour, à avaler avec un verre d'eau",
            "warning": "Ne pas prendre plus de 20",
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        declaration = Declaration.objects.get(pk=response.json()["id"])
        conditions_not_recommended = declaration.conditions_not_recommended.all()
        self.assertIn(conditions[0], conditions_not_recommended)
        self.assertIn(conditions[1], conditions_not_recommended)
        self.assertNotIn(conditions[2], conditions_not_recommended)

        declaration_populations = declaration.populations.all()
        self.assertIn(populations[0], declaration_populations)
        self.assertIn(populations[1], declaration_populations)
        self.assertNotIn(populations[2], declaration_populations)

        self.assertEqual(declaration.company, company)
        self.assertEqual(declaration.address, "243 rue Victor Hugo")
        self.assertEqual(declaration.additional_details, "Deuxième étage")
        self.assertEqual(declaration.postal_code, "69004")
        self.assertEqual(declaration.city, "Lyon")
        self.assertEqual(declaration.cedex, "Lyon 4")
        self.assertEqual(declaration.country, "FR")

        self.assertEqual(declaration.name, "Extrait de Chaga BIO")
        self.assertEqual(declaration.brand, "Azona Rome")
        self.assertEqual(declaration.gamme, "Vegan")
        self.assertEqual(declaration.flavor, "Myrtille")
        self.assertEqual(
            declaration.description,
            "Ce complément alimentaire naturel est composé d'un extrait de Chaga BIO concentré à 30% polysaccharides hautement dosé pour une efficacité optimale",
        )
        self.assertEqual(declaration.galenic_formulation, galenic_formulation)
        self.assertEqual(declaration.unit_quantity, 500.0)
        self.assertEqual(declaration.unit_measurement, unit)
        self.assertEqual(declaration.conditioning, "Sans chitine, pour une bonne absorption et tolérance digestive")
        self.assertEqual(declaration.daily_recommended_dose, "2")
        self.assertEqual(declaration.minimum_duration, "1 mois")
        self.assertEqual(declaration.instructions, "Prendre 1 à 2 gélules par jour, à avaler avec un verre d'eau")
        self.assertEqual(declaration.warning, "Ne pas prendre plus de 20")
        self.assertEqual(declaration.other_effects, "Moduler les défenses naturelles")

        self.assertIn(effect1, declaration.effects.all())
        self.assertIn(effect2, declaration.effects.all())

        self.assertEqual(declaration.author, authenticate.user)

    @authenticate
    def test_create_declaration_declared_plants(self):
        """
        Création de l'objet « déclaration » avec les données de la composition,
        focus sur les plantes
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        plant = PlantFactory()
        plant_part = PlantPartFactory()
        plant.plant_parts.add(plant_part)
        unit = SubstanceUnitFactory()

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredPlants": [
                {
                    "element": {
                        "id": plant.id,
                        "name": plant.name,
                    },
                    "new": False,
                    "active": True,
                    "usedPart": plant_part.id,
                    "quantity": "123",
                    "preparation": "Teinture",
                    "unit": unit.id,
                },
                {
                    "newName": "New plant name",
                    "newDescription": "New plant description",
                    "new": True,
                    "active": True,
                    "usedPart": plant_part.id,
                    "quantity": "890",
                    "preparation": "Autre",
                    "unit": unit.id,
                },
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        declaration = Declaration.objects.get(pk=response.json()["id"])

        self.assertEqual(declaration.declared_plants.count(), 2)

        existing_declared_plant = declaration.declared_plants.get(new=False)
        new_declared_plant = declaration.declared_plants.get(new=True)

        self.assertEqual(existing_declared_plant.plant, plant)
        self.assertEqual(existing_declared_plant.active, True)
        self.assertEqual(existing_declared_plant.used_part, plant_part)
        self.assertEqual(existing_declared_plant.quantity, 123)
        self.assertEqual(existing_declared_plant.unit, unit)
        self.assertEqual(existing_declared_plant.preparation, "Teinture")

        self.assertIsNone(new_declared_plant.plant)
        self.assertEqual(new_declared_plant.new_name, "New plant name")
        self.assertEqual(new_declared_plant.new_description, "New plant description")
        self.assertEqual(new_declared_plant.active, True)
        self.assertEqual(new_declared_plant.used_part, plant_part)
        self.assertEqual(new_declared_plant.quantity, 890)
        self.assertEqual(existing_declared_plant.unit, unit)
        self.assertEqual(new_declared_plant.preparation, "Autre")

    @authenticate
    def test_create_declaration_unknown_plant(self):
        """
        Si la plante spécifié n'existe pas, on doit lever une erreur
        """

        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredPlants": [
                {
                    "element": {
                        "id": 999999,
                    },
                }
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        self.assertIn("declaredPlants", body.get("fieldErrors"))

    @authenticate
    def test_create_declaration_declared_microorganisms(self):
        """
        Création de l'objet « déclaration » avec les données de la composition,
        focus sur les micro-organismes
        """

        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        microorganism = MicroorganismFactory()

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredMicroorganisms": [
                {
                    "element": {
                        "id": microorganism.id,
                        "name": microorganism.name,
                    },
                    "new": False,
                    "active": True,
                    "souche": "souche",
                    "quantity": "123",
                },
                {
                    "newGenre": "New microorganism genre",
                    "newSpecies": "New microorganism species",
                    "newDescription": "New microorganism description",
                    "new": True,
                    "active": True,
                    "souche": "Nouvelle souche",
                    "quantity": "345",
                    "authorizationMode": "EU",
                    "euReferenceCountry": "IT",
                    "euLegalSource": "Voici le doc",
                    "euDetails": "Voici les détails",
                },
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        declaration = Declaration.objects.get(pk=response.json()["id"])

        self.assertEqual(declaration.declared_microorganisms.count(), 2)

        existing_declared_microorganism = declaration.declared_microorganisms.get(new=False)
        new_declared_microorganism = declaration.declared_microorganisms.get(new=True)

        self.assertEqual(existing_declared_microorganism.microorganism, microorganism)
        self.assertEqual(existing_declared_microorganism.active, True)
        self.assertEqual(existing_declared_microorganism.quantity, 123)
        self.assertEqual(existing_declared_microorganism.souche, "souche")

        self.assertIsNone(new_declared_microorganism.microorganism)
        self.assertEqual(new_declared_microorganism.new_species, "New microorganism species")
        self.assertEqual(new_declared_microorganism.new_genre, "New microorganism genre")
        self.assertEqual(new_declared_microorganism.new_description, "New microorganism description")
        self.assertEqual(new_declared_microorganism.active, True)
        self.assertEqual(new_declared_microorganism.quantity, 345)
        self.assertEqual(new_declared_microorganism.souche, "Nouvelle souche")

        self.assertEqual(new_declared_microorganism.authorization_mode, AuthorizationModes.EU)
        self.assertEqual(new_declared_microorganism.eu_reference_country, CountryChoices.ITALY)
        self.assertEqual(new_declared_microorganism.eu_legal_source, "Voici le doc")
        self.assertEqual(new_declared_microorganism.eu_details, "Voici les détails")

    @authenticate
    def test_create_declaration_unknown_microorganism(self):
        """
        Si le micro-organisme spécifié n'existe pas, on doit lever une erreur
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredMicroorganisms": [
                {
                    "element": {
                        "id": 999999,
                    },
                }
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        self.assertIn("declaredMicroorganisms", body.get("fieldErrors"))

    @authenticate
    def test_create_declaration_declared_ingredients(self):
        """
        Création de l'objet « déclaration » avec les données de la composition,
        focus sur les ingrédients
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        ingredient = IngredientFactory()

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredIngredients": [
                {
                    "element": {
                        "id": ingredient.id,
                        "name": ingredient.name,
                    },
                    "new": False,
                    "active": True,
                },
                {
                    "newName": "New ingredient name",
                    "newDescription": "New ingredient description",
                    "new": True,
                    "active": True,
                    "authorizationMode": "FR",
                    "frReason": "NOVEL_FOOD",
                    "frDetails": "Je le veux",
                },
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        declaration = Declaration.objects.get(pk=response.json()["id"])

        self.assertEqual(declaration.declared_ingredients.count(), 2)

        existing_declared_ingredient = declaration.declared_ingredients.get(new=False)
        new_declared_ingredient = declaration.declared_ingredients.get(new=True)

        self.assertEqual(existing_declared_ingredient.ingredient, ingredient)
        self.assertEqual(existing_declared_ingredient.active, True)

        self.assertIsNone(new_declared_ingredient.ingredient)
        self.assertEqual(new_declared_ingredient.new_name, "New ingredient name")
        self.assertEqual(new_declared_ingredient.new_description, "New ingredient description")
        self.assertEqual(new_declared_ingredient.active, True)
        self.assertEqual(new_declared_ingredient.authorization_mode, AuthorizationModes.FR)
        self.assertEqual(new_declared_ingredient.fr_reason, FrAuthorizationReasons.NOVEL_FOOD)
        self.assertEqual(new_declared_ingredient.fr_details, "Je le veux")

    @authenticate
    def test_create_declaration_unknown_ingredient(self):
        """
        Si l'ingrédient spécifié n'existe pas, on doit lever une erreur
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredIngredients": [
                {
                    "element": {
                        "id": 999999,
                    },
                }
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        self.assertIn("declaredIngredients", body.get("fieldErrors"))

    @authenticate
    def test_create_declaration_declared_substances(self):
        """
        Création de l'objet « déclaration » avec les données de la composition,
        focus sur les substances
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        substance = SubstanceFactory()

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredSubstances": [
                {
                    "element": {
                        "id": substance.id,
                        "name": substance.name,
                    },
                    "active": True,
                }
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        declaration = Declaration.objects.get(pk=response.json()["id"])

        self.assertEqual(declaration.declared_substances.count(), 1)

        existing_declared_substance = declaration.declared_substances.first()

        self.assertEqual(existing_declared_substance.substance, substance)
        self.assertEqual(existing_declared_substance.active, True)

    @authenticate
    def test_create_declaration_unknown_substance(self):
        """
        Si la substance spécifiée n'existe pas, on doit lever une erreur
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredSubstances": [
                {
                    "element": {
                        "id": 999999,
                    },
                }
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        self.assertIn("declaredSubstances", body.get("fieldErrors"))

    @authenticate
    def test_create_declaration_computed_substances(self):
        """
        Création de l'objet « déclaration » avec les données de la composition,
        focus sur les substances générées à partir des autres éléments
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        substance = SubstanceFactory()
        unit = SubstanceUnitFactory()

        payload = {
            "name": "Name",
            "company": company.id,
            "computedSubstances": [
                {
                    "substance": {
                        "id": substance.id,
                        "name": substance.name,
                    },
                    "quantity": "123",
                    "unit": unit.id,
                }
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        declaration = Declaration.objects.get(pk=response.json()["id"])

        self.assertEqual(declaration.computed_substances.count(), 1)

        existing_declared_substance = declaration.computed_substances.first()

        self.assertEqual(existing_declared_substance.substance, substance)
        self.assertEqual(existing_declared_substance.quantity, 123)
        self.assertEqual(existing_declared_substance.unit, unit)

    @authenticate
    def test_create_declaration_attachments(self):
        """
        Création de l'objet « déclaration » avec les données de la composition,
        focus sur les pièces jointes
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        current_dir = os.path.dirname(os.path.realpath(__file__))

        blue_image_base_64 = None
        with open(os.path.join(current_dir, "files/Blue.jpg"), "rb") as image:
            blue_image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        green_image_base_64 = None
        with open(os.path.join(current_dir, "files/Green.jpg"), "rb") as image:
            green_image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "name": "Name",
            "company": company.id,
            "attachments": [
                {
                    "file": f"data:image/jpeg;base64,{blue_image_base_64}",
                    "type": "REGULATORY_PROOF",
                },
                {
                    "file": f"data:image/jpeg;base64,{green_image_base_64}",
                    "type": "CERTIFICATE_AUTHORITY",
                },
            ],
        }

        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        declaration = Declaration.objects.get(pk=response.json()["id"])

        self.assertEqual(declaration.attachments.count(), 2)

        self.maxDiff = None

        regulatory_proof = declaration.attachments.get(type=Attachment.AttachmentType.REGULATORY_PROOF)
        saved_regulatory_proof_image = base64.b64encode(regulatory_proof.file.file.file.read()).decode("utf-8")
        self.assertEqual(saved_regulatory_proof_image, blue_image_base_64)

        certificate_authority = declaration.attachments.get(type=Attachment.AttachmentType.CERTIFICATE_AUTHORITY)
        saved_certificate_authority_image = base64.b64encode(certificate_authority.file.file.file.read()).decode(
            "utf-8"
        )
        self.assertEqual(saved_certificate_authority_image, green_image_base_64)

    @authenticate
    def test_retrieve_update_declaration_list(self):
        """
        Un user peut récupérer ses propres déclarations
        """

        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        user_declaration_1 = DeclarationFactory.create(author=authenticate.user, company=company)
        user_declaration_2 = DeclarationFactory.create(author=authenticate.user, company=company)

        other_declaration = DeclarationFactory.create()

        response = self.client.get(reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        declarations = response.json()

        self.assertEqual(len(declarations), 2)
        ids = map(lambda x: x["id"], declarations)
        self.assertIn(user_declaration_1.id, ids)
        self.assertIn(user_declaration_2.id, ids)
        self.assertNotIn(other_declaration.id, ids)

    @authenticate
    def test_retrieve_single_declaration(self):
        """
        Un user peut récupérer les informations complètes d'une de leurs déclarations
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        user_declaration = DeclarationFactory(author=authenticate.user, company=company)
        other_declaration = DeclarationFactory()

        response = self.client.get(reverse("api:retrieve_update_declaration", kwargs={"pk": user_declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("api:retrieve_update_declaration", kwargs={"pk": other_declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_update_single_declaration(self):
        """
        Un user peut modifier les données de sa déclaration
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        user_declaration = DeclarationFactory(author=authenticate.user, name="Old name", company=company)

        payload = {"name": "New name", "company": user_declaration.company.id}
        response = self.client.put(
            reverse("api:retrieve_update_declaration", kwargs={"pk": user_declaration.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_declaration.refresh_from_db()
        self.assertEqual(user_declaration.name, "New name")

    @authenticate
    def test_submit_declaration(self):
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Si un champ obligatoire pour l'instruction manque, on le spécifie
        missing_field_declaration = InstructionReadyDeclarationFactory(
            author=authenticate.user, daily_recommended_dose="", company=company
        )
        response = self.client.post(
            reverse("api:submit_declaration", kwargs={"pk": missing_field_declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_errors = response.json()
        self.assertEqual(len(json_errors["fieldErrors"]), 1)
        self.assertIn("dailyRecommendedDose", json_errors["fieldErrors"][0])

        # S'il n'y a pas d'éléments dans la déclaration, on ne peut pas la soumettre pour instruction
        missing_elements_declaration = InstructionReadyDeclarationFactory(
            author=authenticate.user, declared_plants=[], company=company
        )
        response = self.client.post(
            reverse("api:submit_declaration", kwargs={"pk": missing_elements_declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_errors = response.json()
        self.assertEqual(len(json_errors["nonFieldErrors"]), 1)
        self.assertEqual("Le complément doit comporter au moins un ingrédient", json_errors["nonFieldErrors"][0])

    @authenticate
    def test_submit_declaration_wrong_company(self):
        DeclarantRoleFactory(user=authenticate.user)
        wrong_company = CompanyFactory()

        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=wrong_company)
        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_all_declarations(self):
        """
        Un utilisateur ayant le rôle d'instruction peut récuperer tous les déclarations
        """
        InstructionRoleFactory(user=authenticate.user)

        for _ in range(3):
            DeclarationFactory()
        response = self.client.get(reverse("api:list_all_declarations"), format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

    @authenticate
    def test_get_all_declarations_non_admin(self):
        """
        Un utilisateur n'ayant pas le rôle d'instruction ne pourra pas obtenir toutes les
        déclarations
        """
        for _ in range(3):
            DeclarationFactory()
        response = self.client.get(reverse("api:list_all_declarations"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_filter_author_all_declarations(self):
        """
        Les déclarations peuvent être filtrées par auteur
        """
        InstructionRoleFactory(user=authenticate.user)

        emma = DeclarantRoleFactory()
        edouard = DeclarantRoleFactory()
        stephane = DeclarantRoleFactory()

        [DeclarationFactory(author=edouard.user) for _ in range(4)]
        emma_declarations = [DeclarationFactory(author=emma.user) for _ in range(3)]
        stephane_declarations = [DeclarationFactory(author=stephane.user) for _ in range(5)]

        # Filtrage pour obtenir les déclarations d'Emma
        emma_filter_url = f"{reverse('api:list_all_declarations')}?author={emma.user.id}"
        response = self.client.get(emma_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        for result in results:
            self.assertIn(result["id"], map(lambda x: x.id, emma_declarations))

        # Filtrage pour obtenir les déclarations d'Emma et Edouard, mais pas Stéphane
        emma_edouard_filter_url = f"{reverse('api:list_all_declarations')}?author={emma.user.id},{edouard.user.id}"
        response = self.client.get(emma_edouard_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 7)

        for result in results:
            self.assertNotIn(result["id"], map(lambda x: x.id, stephane_declarations))

    @authenticate
    def test_filter_company_all_declarations(self):
        """
        Les déclarations peuvent être filtrées par entreprise
        """
        InstructionRoleFactory(user=authenticate.user)

        buy_n_large = CompanyFactory()
        acme = CompanyFactory()
        wonka_industries = CompanyFactory()

        [DeclarationFactory(company=buy_n_large) for _ in range(4)]
        acme_declarations = [DeclarationFactory(company=acme) for _ in range(3)]
        wonka_declarations = [DeclarationFactory(company=wonka_industries) for _ in range(5)]

        # Filtrage pour obtenir les déclarations de l'entreprise Acme
        acme_filter_url = f"{reverse('api:list_all_declarations')}?company={acme.id}"
        response = self.client.get(acme_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        for result in results:
            self.assertIn(result["id"], map(lambda x: x.id, acme_declarations))

        # Filtrage pour obtenir les déclarations de Acme et Buy'N'Large, mais pas Wonka Industries
        acme_bnl_filter_url = f"{reverse('api:list_all_declarations')}?company={acme.id},{buy_n_large.id}"
        response = self.client.get(acme_bnl_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 7)

        for result in results:
            self.assertNotIn(result["id"], map(lambda x: x.id, wonka_declarations))

    @authenticate
    def test_filter_status_all_declarations(self):
        """
        Les déclarations peuvent être filtrées par status
        """
        InstructionRoleFactory(user=authenticate.user)

        [DeclarationFactory(status=Declaration.DeclarationStatus.APPROVED) for _ in range(3)]
        [DeclarationFactory(status=Declaration.DeclarationStatus.REJECTED) for _ in range(3)]

        # Filtrage pour obtenir les déclarations approuvées
        spproved_filter_url = f"{reverse('api:list_all_declarations')}?status=APPROVED"
        response = self.client.get(spproved_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        for result in results:
            self.assertEqual(result["status"], Declaration.DeclarationStatus.APPROVED.value)
