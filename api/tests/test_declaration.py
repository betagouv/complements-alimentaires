import base64
import os
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from data.choices import AuthorizationModes, CountryChoices, FrAuthorizationReasons
from data.factories import (
    AwaitingInstructionDeclarationFactory,
    AwaitingVisaDeclarationFactory,
    CompanyFactory,
    ConditionFactory,
    DeclarantRoleFactory,
    DeclarationFactory,
    DeclaredIngredientFactory,
    DeclaredMicroorganismFactory,
    DeclaredPlantFactory,
    DeclaredSubstanceFactory,
    EffectFactory,
    GalenicFormulationFactory,
    IngredientFactory,
    InstructionRoleFactory,
    MicroorganismFactory,
    OngoingInstructionDeclarationFactory,
    OngoingVisaDeclarationFactory,
    PlantFactory,
    PlantPartFactory,
    PopulationFactory,
    PreparationFactory,
    SnapshotFactory,
    SubstanceFactory,
    SubstanceUnitFactory,
    SupervisorRoleFactory,
    VisaRoleFactory,
    PlantSynonymFactory,
)
from data.models import Attachment, Declaration, Snapshot, DeclaredMicroorganism, DeclaredPlant

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
    def test_create_mandated_company_declaration(self):
        """
        Un·e déclarant·e doit pouvoir créer des déclarations pour une compagnie representée
        """
        company = CompanyFactory()
        mandated_company = CompanyFactory()
        company.mandated_companies.add(mandated_company)
        company.save()

        DeclarantRoleFactory(user=authenticate.user, company=mandated_company)

        payload = {
            "company": company.id,
            "name": "name",
        }
        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        preparation_teinture = PreparationFactory(ca_name="Teinture")
        preparation_autre = PreparationFactory(ca_name="Autre macérât")

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
                    "preparation": preparation_teinture.id,
                    "unit": unit.id,
                },
                {
                    "newName": "New plant name",
                    "newDescription": "New plant description",
                    "new": True,
                    "active": True,
                    "usedPart": plant_part.id,
                    "quantity": "890",
                    "preparation": preparation_autre.id,
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
        self.assertEqual(existing_declared_plant.preparation.name, "Teinture")

        self.assertIsNone(new_declared_plant.plant)
        self.assertEqual(new_declared_plant.new_name, "New plant name")
        self.assertEqual(new_declared_plant.new_description, "New plant description")
        self.assertEqual(new_declared_plant.active, True)
        self.assertEqual(new_declared_plant.used_part, plant_part)
        self.assertEqual(new_declared_plant.quantity, 890)
        self.assertEqual(existing_declared_plant.unit, unit)
        self.assertEqual(new_declared_plant.preparation.name, "Autre macérât")

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
        self.assertEqual(
            body["fieldErrors"]["declaredPlants"], "L'ingrédient avec l'id « 999999 » spécifiée n'existe pas."
        )

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
                    "strain": "souche",
                    "quantity": "123",
                },
                {
                    "newGenre": "New microorganism genre",
                    "newSpecies": "New microorganism species",
                    "newDescription": "New microorganism description",
                    "new": True,
                    "active": True,
                    "strain": "Nouvelle souche",
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
        self.assertEqual(existing_declared_microorganism.strain, "souche")

        self.assertIsNone(new_declared_microorganism.microorganism)
        self.assertEqual(new_declared_microorganism.new_species, "New microorganism species")
        self.assertEqual(new_declared_microorganism.new_genre, "New microorganism genre")
        self.assertEqual(new_declared_microorganism.new_description, "New microorganism description")
        self.assertEqual(new_declared_microorganism.active, True)
        self.assertEqual(new_declared_microorganism.quantity, 345)
        self.assertEqual(new_declared_microorganism.strain, "Nouvelle souche")

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
                },
                {
                    "newName": "New substance name",
                    "newDescription": "New substance description",
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

        self.assertEqual(declaration.declared_substances.count(), 2)

        existing_declared_substance = declaration.declared_substances.first()
        new_declared_substance = declaration.declared_substances.get(new=True)

        self.assertEqual(existing_declared_substance.substance, substance)
        self.assertEqual(existing_declared_substance.active, True)

        self.assertIsNone(new_declared_substance.substance)
        self.assertEqual(new_declared_substance.new_name, "New substance name")
        self.assertEqual(new_declared_substance.new_description, "New substance description")
        self.assertEqual(new_declared_substance.active, True)
        self.assertEqual(new_declared_substance.authorization_mode, AuthorizationModes.FR)
        self.assertEqual(new_declared_substance.fr_reason, FrAuthorizationReasons.NOVEL_FOOD)
        self.assertEqual(new_declared_substance.fr_details, "Je le veux")

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
    def test_retrieve_update_destroy_declaration_list(self):
        """
        Un user peut récupérer ses propres déclarations et celles des entreprises pour lesquelles
        iel a des droits.
        """

        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        user_declaration_1 = DeclarationFactory.create(author=authenticate.user, company=company)
        company_declaration_1 = DeclarationFactory.create(company=company)

        other_declaration = DeclarationFactory.create()

        response = self.client.get(reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        declarations = response.json()["results"]

        self.assertEqual(len(declarations), 2)
        ids = list(map(lambda x: x["id"], declarations))
        self.assertIn(user_declaration_1.id, ids)
        self.assertIn(company_declaration_1.id, ids)
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

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": other_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_retrieve_single_declaration_same_company(self):
        """
        Un user ayant le rôle de déclarant·e pour la même entreprise peut récupérer
        les infos de la déclaration
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        user_declaration = DeclarationFactory(company=company)

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_retrieve_single_declaration_supervisor_company(self):
        """
        Un user ayant le rôle de supervision pour la même entreprise peut récupérer
        les infos de la déclaration
        """
        supervisor_role = SupervisorRoleFactory(user=authenticate.user)
        company = supervisor_role.company
        user_declaration = DeclarationFactory(company=company)

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_retrieve_single_declaration_mandated_company(self):
        """
        Un user ayant le rôle de déclaration pour l'entreprise mandatée peut recupérer
        les infos de la déclaration
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        user_declaration = DeclarationFactory(mandated_company=company)

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_retrieve_single_declaration_mandated_company_supervisor(self):
        """
        Un user ayant le rôle de supervision pour l'entreprise mandatée peut recupérer
        les infos de la déclaration
        """
        supervision_role = SupervisorRoleFactory(user=authenticate.user)
        company = supervision_role.company
        user_declaration = DeclarationFactory(mandated_company=company)

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_retrieve_company_declaration(self):
        """
        Un user peut récupérer les informations complètes d'une déclaration de sa
        compagnie
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        company_declaration = DeclarationFactory(company=company)
        other_declaration = DeclarationFactory()

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": company_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": other_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # @authenticate
    # def test_private_notes_instruction(self):
    #     """
    #     Seulement les roles Instruction et Visa peuvent voir les notes privées
    #     """
    #     DeclarantRoleFactory(user=authenticate.user)
    #     declaration = DeclarationFactory(author=authenticate.user)

    #     response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
    #     json_declaration = response.json()
    #     self.assertFalse("privateNotesInstruction" in json_declaration)
    #     self.assertFalse("privateNotesVisa" in json_declaration)

    #     # On essaie à nouveau cette fois ci en étant aussi instructeur·ice
    #     InstructionRoleFactory(user=authenticate.user)
    #     response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
    #     json_declaration = response.json()
    #     self.assertTrue("privateNotesInstruction" in json_declaration)
    #     self.assertTrue("privateNotesVisa" in json_declaration)
    #     self.assertEqual(json_declaration["privateNotesInstruction"], declaration.private_notes_instruction)
    #     self.assertEqual(json_declaration["privateNotesVisa"], declaration.private_notes_visa)

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
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id}),
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_declaration.refresh_from_db()
        self.assertEqual(user_declaration.name, "New name")

    @authenticate
    def test_update_single_declaration_supervisor(self):
        """
        Un superviseur ne peut pas modifier les données de la déclaration d'un·e
        déclarant·e de son entreprise.
        """
        supervisor_role = SupervisorRoleFactory(user=authenticate.user)
        company = supervisor_role.company
        user_declaration = DeclarationFactory(name="Old name", company=company)

        response = self.client.put(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id}),
            {"name": "New name"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_private_comments_user(self):
        """
        Un usager ne peut ni visualiser ni modifier les champs des notes privées
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        declaration = DeclarationFactory(
            author=authenticate.user, company=company, status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION
        )

        # Un usager sans rôles instruction ou visa ne peut pas visualiser les notes privées
        response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
        json_declaration = response.json()
        self.assertFalse("privateNotesInstruction" in json_declaration)
        self.assertFalse("privateNotesVisa" in json_declaration)

        # Un usager sans rôles instruction ou visa ne peut pas modifier les notes privées
        response = self.client.patch(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}),
            {"privateNotesInstruction": "modified by user"},
            format="json",
        )
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.private_notes_instruction, "modified by user")

        response = self.client.patch(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}),
            {"privateNotesVisa": "modified by user"},
            format="json",
        )
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.private_notes_visa, "modified by user")

    @authenticate
    def test_private_comments_instruction(self):
        """
        Une instructrice peut voir les champs de notes privées et modifier le champ
        private_notes_instruction
        """
        InstructionRoleFactory(user=authenticate.user)
        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        # Une instructrice peut visualiser les notes privées
        response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
        json_declaration = response.json()
        self.assertTrue("privateNotesInstruction" in json_declaration)
        self.assertTrue("privateNotesVisa" in json_declaration)

        # Une instructrice peut modifier les notes privées de l'instruction
        response = self.client.patch(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}),
            {"privateNotesInstruction": "modified by instructor"},
            format="json",
        )
        declaration.refresh_from_db()
        self.assertEqual(declaration.private_notes_instruction, "modified by instructor")

        # Une instructrice ne peut pas modifier les notes privées du visa
        response = self.client.patch(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}),
            {"privateNotesVisa": "modified by instructor"},
            format="json",
        )
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.private_notes_visa, "modified by instructor")

    @authenticate
    def test_private_comments_visa(self):
        """
        Une viseuse peut voir les champs de notes privées et modifier le champ
        private_notes_visa
        """
        VisaRoleFactory(user=authenticate.user)
        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        # Une viseuse peut visualiser les notes privées
        response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
        json_declaration = response.json()
        self.assertTrue("privateNotesInstruction" in json_declaration)
        self.assertTrue("privateNotesVisa" in json_declaration)

        # Une viseuse ne peut pas modifier les notes privées de l'instruction
        response = self.client.patch(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}),
            {"privateNotesInstruction": "modified by visor"},
            format="json",
        )
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.private_notes_instruction, "modified by visor")

        # Une instructrice peut modifier les notes privées du visa
        response = self.client.patch(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}),
            {"privateNotesVisa": "modified by visor"},
            format="json",
        )
        declaration.refresh_from_db()
        self.assertEqual(declaration.private_notes_visa, "modified by visor")

    @authenticate
    def test_get_all_declarations(self):
        """
        Un utilisateur ayant le rôle d'instruction peut récuperer toutes les déclarations
        """
        InstructionRoleFactory(user=authenticate.user)

        for _ in range(3):
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        response = self.client.get(reverse("api:list_all_declarations"), format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

    @authenticate
    def test_get_all_declarations_visor(self):
        """
        Un utilisateur ayant le rôle de visa peut récuperer toutes les déclarations
        """
        VisaRoleFactory(user=authenticate.user)

        for _ in range(3):
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        response = self.client.get(reverse("api:list_all_declarations"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

    @authenticate
    def test_get_all_declarations_non_instructor(self):
        """
        Un utilisateur n'ayant pas le rôle d'instruction ne pourra pas obtenir toutes les
        déclarations
        """
        for _ in range(3):
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
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

        [
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, author=edouard.user)
            for _ in range(4)
        ]
        emma_declarations = [
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, author=emma.user)
            for _ in range(3)
        ]
        stephane_declarations = [
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, author=stephane.user)
            for _ in range(5)
        ]

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
    def test_pagination_returns_instructors_and_visors(self):
        """
        La réponse à l'appel API contient les instructrices et viseuses assignées
        """
        InstructionRoleFactory(user=authenticate.user)

        emma = InstructionRoleFactory()
        edouard = InstructionRoleFactory()
        stephane = InstructionRoleFactory()

        anna = VisaRoleFactory()
        quentin = VisaRoleFactory()
        daniel = VisaRoleFactory()

        OngoingInstructionDeclarationFactory(instructor=edouard, visor=anna)
        OngoingInstructionDeclarationFactory(instructor=emma, visor=quentin)
        OngoingInstructionDeclarationFactory(instructor=stephane, visor=daniel)

        response = self.client.get(reverse("api:list_all_declarations"), format="json")
        instructors = response.json()["instructors"]
        visors = response.json()["visors"]

        for instructor in [emma, edouard, stephane]:
            json_instructor = next(filter(lambda x: x["id"] == instructor.id, instructors), None)
            self.assertIsNotNone(json_instructor)
            self.assertAlmostEqual(json_instructor["name"], instructor.name)

        for visor in [anna, quentin, daniel]:
            json_visor = next(filter(lambda x: x["id"] == visor.id, visors), None)
            self.assertIsNotNone(json_visor)
            self.assertAlmostEqual(json_visor["name"], visor.name)

    @authenticate
    def test_filter_instructor_all_declarations(self):
        """
        Les déclarations peuvent être filtrées par instructrice
        """
        InstructionRoleFactory(user=authenticate.user)

        emma = InstructionRoleFactory()
        edouard = InstructionRoleFactory()
        stephane = InstructionRoleFactory()

        emma_declaration = OngoingInstructionDeclarationFactory(instructor=emma)
        OngoingInstructionDeclarationFactory(instructor=edouard)
        OngoingInstructionDeclarationFactory(instructor=stephane)

        emma_filter_url = f"{reverse('api:list_all_declarations')}?instructor={emma.id}"
        response = self.client.get(emma_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], emma_declaration.id)

    @authenticate
    def test_filter_instructor_not_assigned(self):
        """
        Les déclarations peuvent être filtrées par celles qui n'ont pas encore d'instructrice
        """
        InstructionRoleFactory(user=authenticate.user)

        emma = InstructionRoleFactory()
        edouard = InstructionRoleFactory()
        stephane = InstructionRoleFactory()

        OngoingInstructionDeclarationFactory(instructor=emma)
        OngoingInstructionDeclarationFactory(instructor=edouard)
        OngoingInstructionDeclarationFactory(instructor=stephane)
        declaration = AwaitingInstructionDeclarationFactory()

        unassigned_filter_url = f"{reverse('api:list_all_declarations')}?instructor=None"
        response = self.client.get(unassigned_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)

    @authenticate
    def test_ordering_and_filtering_instructor_not_assigned(self):
        """
        Le filtre des non-assignés doit pouvoir s'effectuer avec celui du triage
        """
        InstructionRoleFactory(user=authenticate.user)

        emma = InstructionRoleFactory()
        edouard = InstructionRoleFactory()
        stephane = InstructionRoleFactory()

        OngoingInstructionDeclarationFactory(instructor=emma)
        OngoingInstructionDeclarationFactory(instructor=edouard)
        OngoingInstructionDeclarationFactory(instructor=stephane)
        declaration = AwaitingInstructionDeclarationFactory()

        url = f"{reverse('api:list_all_declarations')}?instructor=None&ordering=responseLimitDate"
        response = self.client.get(url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)

    @authenticate
    def test_filter_instructor_not_assigned_and_assigned(self):
        """
        Les déclarations peuvent être filtrées par celles qui n'ont pas encore d'instructrice
        et par une instructrice en particulier en même temps
        """
        InstructionRoleFactory(user=authenticate.user)

        emma = InstructionRoleFactory()
        edouard = InstructionRoleFactory()
        stephane = InstructionRoleFactory()

        emma_declaration = OngoingInstructionDeclarationFactory(instructor=emma)
        OngoingInstructionDeclarationFactory(instructor=edouard)
        OngoingInstructionDeclarationFactory(instructor=stephane)
        unassigned_declaration = AwaitingInstructionDeclarationFactory()

        filter_url = f"{reverse('api:list_all_declarations')}?instructor=None,{emma.id}"
        response = self.client.get(filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 2)

        self.assertIsNotNone(next(filter(lambda x: x["id"] == emma_declaration.id, results), None))
        self.assertIsNotNone(next(filter(lambda x: x["id"] == unassigned_declaration.id, results), None))

    @authenticate
    def test_filter_visor_all_declarations(self):
        """
        Les déclarations peuvent être filtrées par viseuse
        """
        VisaRoleFactory(user=authenticate.user)

        emma = VisaRoleFactory()
        edouard = VisaRoleFactory()
        stephane = VisaRoleFactory()

        emma_declaration = OngoingInstructionDeclarationFactory(visor=emma)
        OngoingInstructionDeclarationFactory(visor=edouard)
        OngoingInstructionDeclarationFactory(visor=stephane)

        emma_filter_url = f"{reverse('api:list_all_declarations')}?visor={emma.id}"
        response = self.client.get(emma_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], emma_declaration.id)

    @authenticate
    def test_filter_visor_not_assigned(self):
        """
        Les déclarations peuvent être filtrées par celles qui n'ont pas encore de viseuse
        """
        VisaRoleFactory(user=authenticate.user)

        emma = VisaRoleFactory()
        edouard = VisaRoleFactory()
        stephane = VisaRoleFactory()

        OngoingInstructionDeclarationFactory(visor=emma)
        OngoingInstructionDeclarationFactory(visor=edouard)
        OngoingInstructionDeclarationFactory(visor=stephane)
        declaration = AwaitingVisaDeclarationFactory()

        unassigned_filter_url = f"{reverse('api:list_all_declarations')}?visor=None"
        response = self.client.get(unassigned_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)

    @authenticate
    def test_filter_visor_not_assigned_and_assigned(self):
        """
        Les déclarations peuvent être filtrées par celles qui n'ont pas encore d'instructrice
        et par une instructrice en particulier en même temps
        """
        VisaRoleFactory(user=authenticate.user)

        emma = VisaRoleFactory()
        edouard = VisaRoleFactory()
        stephane = VisaRoleFactory()

        emma_declaration = OngoingInstructionDeclarationFactory(visor=emma)
        OngoingInstructionDeclarationFactory(visor=edouard)
        OngoingInstructionDeclarationFactory(visor=stephane)
        unassigned_declaration = AwaitingVisaDeclarationFactory()

        filter_url = f"{reverse('api:list_all_declarations')}?visor=None,{emma.id}"
        response = self.client.get(filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 2)

        self.assertIsNotNone(next(filter(lambda x: x["id"] == emma_declaration.id, results), None))
        self.assertIsNotNone(next(filter(lambda x: x["id"] == unassigned_declaration.id, results), None))

    @authenticate
    def test_filter_company_all_declarations(self):
        """
        Les déclarations peuvent être filtrées par entreprise
        """
        InstructionRoleFactory(user=authenticate.user)

        buy_n_large = CompanyFactory()
        acme = CompanyFactory()
        wonka_industries = CompanyFactory()

        [
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, company=buy_n_large)
            for _ in range(4)
        ]
        acme_declarations = [
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, company=acme)
            for _ in range(3)
        ]
        wonka_declarations = [
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, company=wonka_industries)
            for _ in range(5)
        ]

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

        [DeclarationFactory(status=Declaration.DeclarationStatus.AUTHORIZED) for _ in range(3)]
        [DeclarationFactory(status=Declaration.DeclarationStatus.ABANDONED) for _ in range(3)]

        # Filtrage pour obtenir les déclarations approuvées
        authorized_filter_url = f"{reverse('api:list_all_declarations')}?status=AUTHORIZED"
        response = self.client.get(authorized_filter_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        for result in results:
            self.assertEqual(result["status"], Declaration.DeclarationStatus.AUTHORIZED.value)

    @authenticate
    def test_filter_company_name_start_end(self):
        """
        Les déclarations peuvent être filtrées par le nom d'une compagnie : début et fin
        """
        InstructionRoleFactory(user=authenticate.user)
        companies = [
            CompanyFactory(social_name="Àccented Corporation"),
            CompanyFactory(social_name="Compléments santé"),
            CompanyFactory(social_name="lowercase ltd"),
            CompanyFactory(social_name="Soylent Corp"),
            CompanyFactory(social_name="Umbrella Corporation"),
            CompanyFactory(social_name="Zebra Ltd"),
        ]
        for company in companies:
            DeclarationFactory(status=Declaration.DeclarationStatus.AUTHORIZED, company=company)

        # Filtrage pour obtenir les déclarations utilisant le filtre début et fin du social name

        # Tout ce qui vient après la « S » : Soylent Corp, Umbrella Corporation et Zebra Ltd
        url = f"{reverse('api:list_all_declarations')}?company_name_start=S"
        response = self.client.get(url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)
        returned_companies = list(map(lambda x: x["company"]["socialName"], results))
        self.assertIn("Soylent Corp", returned_companies)
        self.assertIn("Umbrella Corporation", returned_companies)
        self.assertIn("Zebra Ltd", returned_companies)

        # De la « A » à la « Co » : Àccented Corporation et Compléments santé
        url = f"{reverse('api:list_all_declarations')}?company_name_start=A&company_name_end=Co"
        response = self.client.get(url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        returned_companies = list(map(lambda x: x["company"]["socialName"], results))
        self.assertIn("Àccented Corporation", returned_companies)
        self.assertIn("Compléments santé", returned_companies)

        # Jusqu'à la « L » : Àccented Corporation, Compléments santé, lowercase ltd
        url = f"{reverse('api:list_all_declarations')}?company_name_end=L"
        response = self.client.get(url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)
        returned_companies = list(map(lambda x: x["company"]["socialName"], results))
        self.assertIn("Àccented Corporation", returned_companies)
        self.assertIn("Compléments santé", returned_companies)
        self.assertIn("lowercase ltd", returned_companies)

        # À partir de « um » (minuscule) : Umbrella Corporation et Zebra Ltd
        url = f"{reverse('api:list_all_declarations')}?company_name_start=ul"
        response = self.client.get(url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        returned_companies = list(map(lambda x: x["company"]["socialName"], results))
        self.assertIn("Umbrella Corporation", returned_companies)
        self.assertIn("Zebra Ltd", returned_companies)

        # De la « y » à la « z » (minuscule) : Zebra Ltd
        url = f"{reverse('api:list_all_declarations')}?company_name_start=y&company_name_end=z"
        response = self.client.get(url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        returned_companies = list(map(lambda x: x["company"]["socialName"], results))
        self.assertIn("Zebra Ltd", returned_companies)

    @authenticate
    def test_filter_by_article(self):
        """
        Les déclarations peuvent être filtrées par article
        """
        InstructionRoleFactory(user=authenticate.user)
        art_15 = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_16)
        AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ANSES_REFERAL)

        # Filtrage pour obtenir les déclarations en article 15
        url = f"{reverse('api:list_all_declarations')}?article=ART_15"
        response = self.client.get(url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], art_15.id)

    @authenticate
    def test_sort_declarations_by_name(self):
        """
        Les déclarations peuvent être triées par nom
        """
        InstructionRoleFactory(user=authenticate.user)
        names = ["B", "C", "A", "D"]

        for name in names:
            DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, name=name)

        # Triage par nom
        name_sort_url = f"{reverse('api:list_all_declarations')}?ordering=name"
        response = self.client.get(name_sort_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 4)

        names.sort()
        for index, expected_name in enumerate(names):
            self.assertEqual(results[index]["name"], expected_name)

        # Triage par nom inversé
        reverse_name_sort_url = f"{reverse('api:list_all_declarations')}?ordering=-name"
        response = self.client.get(reverse_name_sort_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 4)

        names.reverse()
        for index, expected_name in enumerate(names):
            self.assertEqual(results[index]["name"], expected_name)

    @authenticate
    def test_instructor_can_access_declaration(self):
        """
        Les déclarations peuvent être vues par des personnes ayant le rôle instructor
        """
        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        InstructionRoleFactory(user=authenticate.user)

        response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_instructor_does_not_see_drafts(self):
        """
        Les déclarations brouillons ne sont pas visibles aux personnes ayant le rôle instructor
        """
        draft_declaration = DeclarationFactory(status=Declaration.DeclarationStatus.DRAFT)
        InstructionRoleFactory(user=authenticate.user)

        response = self.client.get(reverse("api:list_all_declarations"), format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 0)

        response = self.client.get(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": draft_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_delete_declaration(self):
        """
        Les déclarations en mode brouillon peuvent être supprimées
        """
        draft_declaration = DeclarationFactory(status=Declaration.DeclarationStatus.DRAFT, author=authenticate.user)
        DeclarantRoleFactory(user=authenticate.user, company=draft_declaration.company)

        response = self.client.delete(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": draft_declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(list(Declaration.objects.filter(id=draft_declaration.id))), 0)

    @authenticate
    def test_delete_non_draft_declaration(self):
        """
        Les déclarations en mode brouillon peuvent être supprimées
        """
        declaration = AwaitingInstructionDeclarationFactory(author=authenticate.user)
        DeclarantRoleFactory(user=authenticate.user, company=declaration.company)

        response = self.client.delete(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id})
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(list(Declaration.objects.filter(id=declaration.id))), 1)

    @authenticate
    def test_supervisor_declarations_list_view(self):
        """
        Une view spécifique pour les gestionnaires des entreprises est disponible et doit
        retourner toutes les déclarations non-draft de l'entreprise
        """
        company = CompanyFactory()
        SupervisorRoleFactory(user=authenticate.user, company=company)

        other_company = CompanyFactory()

        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, company=company)
        DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION, company=other_company)

        response = self.client.get(reverse("api:company_declarations_list_view", kwargs={"pk": company.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)

    @authenticate
    def test_sort_declarations_by_instruction_limit(self):
        """
        Les déclarations peuvent être triées par la date limite d'instruction
        """
        InstructionRoleFactory(user=authenticate.user)

        today = timezone.now()

        declaration_middle = AwaitingInstructionDeclarationFactory()
        snapshot_middle = SnapshotFactory(declaration=declaration_middle, status=declaration_middle.status)
        snapshot_middle.creation_date = today - timedelta(days=5)
        snapshot_middle.save()

        declaration_first = AwaitingInstructionDeclarationFactory()
        snapshot_first = SnapshotFactory(declaration=declaration_first, status=declaration_first.status)
        snapshot_first.creation_date = today - timedelta(days=1)
        snapshot_first.save()

        declaration_last = AwaitingInstructionDeclarationFactory()
        snapshot_last = SnapshotFactory(declaration=declaration_last, status=declaration_last.status)
        snapshot_last.creation_date = today - timedelta(days=10)
        snapshot_last.save()

        # Triage par date limite d'instruction
        sort_url = f"{reverse('api:list_all_declarations')}?ordering=responseLimitDate"
        response = self.client.get(sort_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        self.assertEqual(results[0]["id"], declaration_last.id)
        self.assertEqual(results[1]["id"], declaration_middle.id)
        self.assertEqual(results[2]["id"], declaration_first.id)

        # Triage par date limite d'instruction inversé
        reverse_sort_url = f"{reverse('api:list_all_declarations')}?ordering=-responseLimitDate"
        response = self.client.get(reverse_sort_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        self.assertEqual(results[0]["id"], declaration_first.id)
        self.assertEqual(results[1]["id"], declaration_middle.id)
        self.assertEqual(results[2]["id"], declaration_last.id)

    @authenticate
    def test_update_article(self):
        """
        Les viseuses ou instructrices peuvent changer l'article d'une déclaration
        """
        InstructionRoleFactory(user=authenticate.user)
        art_15 = AwaitingInstructionDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        DeclaredPlantFactory(new=False, declaration=art_15)
        art_15.assign_calculated_article()
        art_15.save()
        art_15.refresh_from_db()

        self.assertEqual(art_15.article, Declaration.Article.ARTICLE_15)

        # Une instructrice peut surcharger l'article

        url = reverse("api:update_article", kwargs={"pk": art_15.id})
        payload = {"article": "ART_16"}
        response = self.client.post(url, payload)
        result = response.json()
        self.assertEqual(result["article"], "ART_16")

        art_15.refresh_from_db()
        self.assertEqual(art_15.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(art_15.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertEqual(art_15.overriden_article, Declaration.Article.ARTICLE_16)

    @authenticate
    def test_update_article_unauthorized(self):
        """
        Les viseuses ou instructrices peuvent changer l'article d'une déclaration, non pas
        les déclarant·e·s
        """
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)
        art_15 = AwaitingInstructionDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
            company=company,
            author=authenticate.user,
        )
        DeclaredPlantFactory(new=False, declaration=art_15)

        url = reverse("api:update_article", kwargs={"pk": art_15.id})

        payload = {"article": "ART_16"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_take_ownership(self):
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)
        declaration = AwaitingInstructionDeclarationFactory(company=company)

        self.assertNotEqual(declaration.author, authenticate.user)

        url = reverse("api:take_authorship", kwargs={"pk": declaration.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.author, authenticate.user)

    @authenticate
    def test_take_ownership_unauthorized(self):
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)
        declaration = AwaitingInstructionDeclarationFactory()

        self.assertNotEqual(declaration.author, authenticate.user)

        url = reverse("api:take_authorship", kwargs={"pk": declaration.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        declaration.refresh_from_db()
        self.assertNotEqual(declaration.author, authenticate.user)

    @authenticate
    def test_visa_refusal_field(self):
        VisaRoleFactory(user=authenticate.user)
        declaration = OngoingVisaDeclarationFactory()
        SnapshotFactory(declaration=declaration, action=Snapshot.SnapshotActions.RESPOND_TO_OBJECTION)
        response = self.client.post(reverse("api:refuse_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("api:list_all_declarations"), format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]["visaRefused"])


class TestDeclaredElementsApi(APITestCase):
    @authenticate
    def test_get_declared_elements(self):
        """
        Les instructrices peuvent voir une liste de toutes les demandes de nouveaux ingredients
        Tous types confondus. Ignorer les déclarations en brouillon
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        draft = DeclarationFactory(status=Declaration.DeclarationStatus.DRAFT)
        for _ in range(3):
            DeclaredPlantFactory(new=True, declaration=declaration)
            DeclaredSubstanceFactory(new=True, declaration=declaration)
            DeclaredMicroorganismFactory(new=True, declaration=declaration)
            DeclaredIngredientFactory(new=True, declaration=declaration)
            # don't return not new ones
            DeclaredPlantFactory(new=False, declaration=declaration)
            # don't return ones attached to draft declarations
            DeclaredIngredientFactory(new=True, declaration=draft)

        response = self.client.get(reverse("api:list_new_declared_elements"), format="json")
        results = response.json()
        self.assertEqual(results["count"], 12)
        result = results["results"][0]
        self.assertEqual(result["declaration"]["id"], declaration.id)

    def test_get_declared_elements_not_allowed_not_authenticated(self):
        response = self.client.get(reverse("api:list_new_declared_elements"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_declared_elements_not_allowed_not_instructor(self):
        response = self.client.get(reverse("api:list_new_declared_elements"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_single_declared_plant(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        plant = DeclaredPlantFactory(declaration=declaration)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": plant.id, "type": "plant"}), format="json"
        )
        body = response.json()
        self.assertEqual(body["id"], plant.id)

    @authenticate
    def test_get_single_declared_microorganism(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        microorganism = DeclaredMicroorganismFactory(declaration=declaration)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": microorganism.id, "type": "microorganism"}), format="json"
        )
        body = response.json()
        self.assertEqual(body["id"], microorganism.id)

    @authenticate
    def test_get_single_declared_substance(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        substance = DeclaredSubstanceFactory(declaration=declaration)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": substance.id, "type": "substance"}), format="json"
        )
        body = response.json()
        self.assertEqual(body["id"], substance.id)

    @authenticate
    def test_get_single_declared_ingredient(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        ingredient = DeclaredIngredientFactory(declaration=declaration)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": ingredient.id, "type": "ingredient"}), format="json"
        )
        body = response.json()
        self.assertEqual(body["id"], ingredient.id)

    @authenticate
    def test_cannot_get_declared_element_unknown_type(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        ingredient = DeclaredIngredientFactory(declaration=declaration)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": ingredient.id, "type": "unknown"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["globalError"],
            "Unknown type: 'unknown' not in ['plant', 'microorganism', 'substance', 'ingredient']",
        )

    def test_get_declared_element_not_allowed_not_authenticated(self):
        response = self.client.get(reverse("api:declared_element", kwargs={"pk": 1, "type": "plant"}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": 1, "type": "microorganism"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": 1, "type": "substance"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": 1, "type": "ingredient"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_declared_element_not_allowed_not_instructor(self):
        response = self.client.get(reverse("api:declared_element", kwargs={"pk": 1, "type": "plant"}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": 1, "type": "microorganism"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": 1, "type": "substance"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element", kwargs={"pk": 1, "type": "ingredient"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_request_info_declared_element(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        microorganism = DeclaredMicroorganismFactory(declaration=declaration)
        self.assertNotEqual(microorganism.request_status, DeclaredMicroorganism.AddableStatus.INFORMATION)

        response = self.client.post(
            reverse("api:declared_element_request_info", kwargs={"pk": microorganism.id, "type": "microorganism"}),
            {"requestPrivateNotes": "some notes"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["requestStatus"], DeclaredMicroorganism.AddableStatus.INFORMATION)
        microorganism.refresh_from_db()
        self.assertEqual(microorganism.request_private_notes, "some notes")
        self.assertEqual(microorganism.request_status, DeclaredMicroorganism.AddableStatus.INFORMATION)

    @authenticate
    def test_request_info_declared_element_not_allowed_not_instructor(self):
        response = self.client.get(
            reverse("api:declared_element_request_info", kwargs={"pk": 1, "type": "plant"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element_request_info", kwargs={"pk": 1, "type": "microorganism"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element_request_info", kwargs={"pk": 1, "type": "substance"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element_request_info", kwargs={"pk": 1, "type": "ingredient"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_reject_declared_element(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        microorganism = DeclaredMicroorganismFactory(declaration=declaration)
        self.assertNotEqual(microorganism.request_status, DeclaredMicroorganism.AddableStatus.REJECTED)

        response = self.client.post(
            reverse("api:declared_element_reject", kwargs={"pk": microorganism.id, "type": "microorganism"}),
            {"requestPrivateNotes": "some notes"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        microorganism.refresh_from_db()
        self.assertEqual(microorganism.request_private_notes, "some notes")
        self.assertEqual(microorganism.request_status, DeclaredMicroorganism.AddableStatus.REJECTED)

    @authenticate
    def test_reject_declared_element_not_allowed_not_instructor(self):
        response = self.client.get(
            reverse("api:declared_element_reject", kwargs={"pk": 1, "type": "plant"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element_reject", kwargs={"pk": 1, "type": "microorganism"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element_reject", kwargs={"pk": 1, "type": "substance"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("api:declared_element_reject", kwargs={"pk": 1, "type": "ingredient"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_fields_hidden_from_declarant(self):
        """
        La déclaration doit pas contenir les champs statut et notes privés pour des ingrédients
        si l'user est un déclarant
        """
        DeclarantRoleFactory(user=authenticate.user)
        declaration = DeclarationFactory(author=authenticate.user)
        microorganism = DeclaredMicroorganismFactory(declaration=declaration)

        response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
        body = response.json()
        declared_microorganisms = body["declaredMicroorganisms"]
        m = declared_microorganisms[0]
        self.assertEqual(m["id"], microorganism.id)
        self.assertNotIn("requestStatus", m)
        self.assertNotIn("requestPrivateNotes", m)

    @authenticate
    def test_status_visible_to_instructor(self):
        """
        La déclaration contient les infos sur le statut de la demande d'un ingrédient.
        Visible aux instructrices et viseurs.
        """
        InstructionRoleFactory(user=authenticate.user)
        declaration = AwaitingInstructionDeclarationFactory()

        response = self.client.get(reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": declaration.id}))
        body = response.json()
        declared_microorganisms = body["declaredMicroorganisms"]
        m = declared_microorganisms[0]
        self.assertIn("requestStatus", m)
        self.assertIn("requestPrivateNotes", m)

    @authenticate
    def test_replace_declared_plant(self):
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration, new=True)
        self.assertNotEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REPLACED)
        plant = PlantFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {"element": {"id": plant.id, "type": "plant"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        declared_plant.refresh_from_db()
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REPLACED)
        self.assertFalse(declared_plant.new)
        self.assertEqual(declared_plant.plant, plant)

    @authenticate
    def test_cannot_replace_element_different_type(self):
        """
        Pour reduire le scope de changements, temporairement bloque le remplacement d'une demande
        avec un element d'un type different
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration)
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REQUESTED)
        microorganism = MicroorganismFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {"element": {"id": microorganism.id, "type": "microorganism"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
        declared_plant.refresh_from_db()
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REQUESTED)
        self.assertNotEqual(declared_plant.plant, microorganism)

    @authenticate
    def test_can_add_synonym_on_replace(self):
        """
        C'est possible d'envoyer une liste avec un nouvel element pour
        ajouter un synonyme et laisser des synonymes existantes non-modifiées
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration, new=True)
        plant = PlantFactory()
        synonym = PlantSynonymFactory.create(name="Eucalyptus Plant", standard_name=plant)

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "synonyms": [{"id": synonym.id, "name": "Eucalyptus Plant"}, {"name": "New synonym"}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        declared_plant.refresh_from_db()
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REPLACED)
        plant.refresh_from_db()
        self.assertEqual(plant.plantsynonym_set.count(), 2)
        self.assertIsNotNone(plant.plantsynonym_set.get(name="New synonym"))
        self.assertEqual(plant.plantsynonym_set.get(id=synonym.id).name, synonym.name)
