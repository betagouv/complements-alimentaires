import base64
import os
from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from data.choices import AuthorizationModes, CountryChoices, FrAuthorizationReasons
from data.factories import (
    AuthorizedDeclarationFactory,
    AwaitingInstructionDeclarationFactory,
    AwaitingVisaDeclarationFactory,
    CompanyFactory,
    ComputedSubstanceFactory,
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
    PlantSynonymFactory,
    PopulationFactory,
    PreparationFactory,
    SnapshotFactory,
    SubstanceFactory,
    SupervisorRoleFactory,
    UnitFactory,
    VisaRoleFactory,
)
from data.models import (
    Addable,
    Attachment,
    Declaration,
    DeclaredMicroorganism,
    DeclaredPlant,
    DeclaredSubstance,
    IngredientStatus,
    IngredientType,
    Part,
    Snapshot,
)

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
        effect1 = EffectFactory(name="Artères et cholestérol")
        effect2 = EffectFactory(name="Autre (à préciser)")
        populations = [PopulationFactory() for _ in range(3)]
        unit = UnitFactory()
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
        unit = UnitFactory()
        preparation_teinture = PreparationFactory(name="Teinture")
        preparation_autre = PreparationFactory(name="Autre macérât")

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
    def test_create_declaration_calculate_article(self):
        """
        Il est possible d'ajouter un query_param pour forcer le calcul de l'article
        dans la sauvegarde
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        PopulationFactory(name="Population générale")
        plant = PlantFactory()
        plant_part = PlantPartFactory()
        plant.plant_parts.add(plant_part)
        unit = UnitFactory()
        preparation_autre = PreparationFactory(name="Autre macérât")

        payload = {
            "name": "Name",
            "company": company.id,
            "declaredPlants": [
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
        # Une requête normale ne calculera pas l'article
        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id}), payload, format="json"
        )
        declaration = Declaration.objects.get(pk=response.json()["id"])
        self.assertIsNone(declaration.article)

        # Maintenant on fait une requête mais en spécifiant qu'on veut recalculer l'article avec
        # le query parameter force-article-calculation=true
        response = self.client.post(
            reverse("api:list_create_declaration", kwargs={"user_pk": authenticate.user.id})
            + "?force-article-calculation=true",
            payload,
            format="json",
        )

        declaration = Declaration.objects.get(pk=response.json()["id"])

        self.assertEqual(declaration.article, Declaration.Article.ARTICLE_16)

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
        self.assertEqual(new_declared_microorganism.new_name, "New microorganism species New microorganism genre")
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
        unit = UnitFactory()

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
    def test_search_list_create_declaration(self):
        """
        Un·e utilisateur·ice peut chercher dans ses propres déclarations et celles des entreprises pour lesquelles
        iel a des droits.
        """

        def get_search_results(search_term):
            response = self.client.get(
                f"{reverse('api:list_create_declaration', kwargs={'user_pk': authenticate.user.id})}?search={search_term}",
                format="json",
            )
            return response.json()["results"]

        umbrella_corp = CompanyFactory(social_name="Umbrella corporation")
        globex = CompanyFactory(social_name="Globex")

        SupervisorRoleFactory(user=authenticate.user, company=umbrella_corp)
        SupervisorRoleFactory(user=authenticate.user, company=globex)

        omega = AwaitingInstructionDeclarationFactory(company=umbrella_corp, name="Omega")
        magnesium = AwaitingInstructionDeclarationFactory(company=umbrella_corp, name="Magnésium")
        fer = AwaitingInstructionDeclarationFactory(company=globex, name="Fer")
        creatine = AwaitingInstructionDeclarationFactory(
            company=globex, name="Créatine", teleicare_declaration_number="old_declaration_number"
        )

        # Checher "globex". Les deux compléments de l'entreprise Globex doivent être renvoyés
        results = get_search_results("Globex")
        self.assertEqual(len(results), 2)
        (self.assertIn(x.id, map(lambda x: x["id"], results)) for x in [fer, creatine])

        # Checher "omega". Seulement omega devrait sortir
        results = get_search_results("omega")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], omega.id)

        # Checher par ID (magnésium)
        results = get_search_results(magnesium.id)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], magnesium.id)

        # Chercher en ignorant les accents (magnésium)
        results = get_search_results("magnesium")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], magnesium.id)

        # Chercher par ID téléicare
        results = get_search_results("old_declaration_number")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], creatine.id)

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
    def test_update_single_declaration_calculating_article(self):
        """
        Il est possible d'ajouter un query_param pour forcer le calcul de l'article
        dans la sauvegarde
        """
        PopulationFactory(name="Population générale")
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        user_declaration = DeclarationFactory(author=authenticate.user, name="Old name", company=company)

        payload = {
            "name": "New name",
            "company": user_declaration.company.id,
            "declaredPlants": [
                {
                    "active": True,
                    "new": True,
                    "newDescription": "as",
                    "newName": "as",
                    "newType": "plant",
                },
            ],
        }
        # Une requête normale ne calculera pas l'article
        self.client.put(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id}),
            payload,
            format="json",
        )
        user_declaration.refresh_from_db()
        self.assertIsNone(user_declaration.article)

        # Maintenant on fait une requête mais en spécifiant qu'on veut recalculer l'article avec
        # le query parameter force-article-calculation=true
        self.client.put(
            reverse("api:retrieve_update_destroy_declaration", kwargs={"pk": user_declaration.id})
            + "?force-article-calculation=true",
            payload,
            format="json",
        )
        user_declaration.refresh_from_db()
        self.assertEqual(user_declaration.article, Declaration.Article.ARTICLE_16)

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
        art_15 = AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_15)
        AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_16)
        AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ANSES_REFERAL)

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
    def test_sort_declarations_by_instruction_limit_with_visa(self):
        """
        Le refus d'un visa ne doit pas compter pour le triage par date limite de réponse
        """
        InstructionRoleFactory(user=authenticate.user)

        today = timezone.now()

        declaration_less_urgent = AwaitingInstructionDeclarationFactory()
        snapshot_less_urgent = SnapshotFactory(
            declaration=declaration_less_urgent, status=declaration_less_urgent.status
        )
        snapshot_less_urgent.creation_date = today - timedelta(days=1)
        snapshot_less_urgent.save()

        declaration_more_urgent = AwaitingInstructionDeclarationFactory()
        snapshot_more_urgent = SnapshotFactory(
            declaration=declaration_more_urgent, status=declaration_more_urgent.status
        )
        snapshot_more_urgent.creation_date = today - timedelta(days=10)
        snapshot_more_urgent.save()

        # Le snapshot du refus de visa ne doit pas affecter la date limite de réponse
        snapshot_visa_refusal = SnapshotFactory(
            declaration=declaration_more_urgent,
            status=declaration_more_urgent.status,
            action=Snapshot.SnapshotActions.REFUSE_VISA,
        )
        snapshot_visa_refusal.creation_date = today - timedelta(days=1)
        snapshot_visa_refusal.save()

        # Triage par date limite d'instruction
        sort_url = f"{reverse('api:list_all_declarations')}?ordering=responseLimitDate"
        response = self.client.get(sort_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 2)

        self.assertEqual(results[0]["id"], declaration_more_urgent.id)
        self.assertEqual(results[1]["id"], declaration_less_urgent.id)

        # Triage par date limite d'instruction inversé
        reverse_sort_url = f"{reverse('api:list_all_declarations')}?ordering=-responseLimitDate"
        response = self.client.get(reverse_sort_url, format="json")
        results = response.json()["results"]
        self.assertEqual(len(results), 2)

        self.assertEqual(results[0]["id"], declaration_less_urgent.id)
        self.assertEqual(results[1]["id"], declaration_more_urgent.id)

    @authenticate
    def test_update_article(self):
        """
        Les viseuses ou instructrices peuvent changer l'article d'une déclaration
        """
        PopulationFactory(name="Population générale")
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
        self.assertEqual(art_15.overridden_article, Declaration.Article.ARTICLE_16)

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
    def test_assign_instruction(self):
        """
        Une instructrice peut à tout moment s'assigner un dossier d'instruction.
        """
        old_instructor = InstructionRoleFactory()
        new_instructor = InstructionRoleFactory(user=authenticate.user)

        declaration = AwaitingInstructionDeclarationFactory(instructor=old_instructor)

        url = reverse("api:assign_instruction", kwargs={"pk": declaration.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.instructor, new_instructor)

    @authenticate
    def test_assign_instruction_unauthorized(self):
        old_instructor = InstructionRoleFactory()

        declaration = AwaitingInstructionDeclarationFactory(instructor=old_instructor)

        url = reverse("api:assign_instruction", kwargs={"pk": declaration.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        declaration.refresh_from_db()
        self.assertEqual(declaration.instructor, old_instructor)

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

    @authenticate
    def test_search_fields(self):
        def get_search_results(search_term):
            response = self.client.get(f"{reverse('api:list_all_declarations')}?search={search_term}", format="json")
            return response.json()["results"]

        InstructionRoleFactory(user=authenticate.user)

        umbrella_corp = CompanyFactory(social_name="Umbrella corporation")
        globex = CompanyFactory(social_name="Globex")

        omega = AwaitingInstructionDeclarationFactory(company=umbrella_corp, name="Omega")
        magnesium = AwaitingInstructionDeclarationFactory(company=umbrella_corp, name="Magnésium")

        fer = AwaitingInstructionDeclarationFactory(company=globex, name="Fer")
        creatine = AwaitingInstructionDeclarationFactory(
            company=globex, name="Créatine", teleicare_declaration_number="old_declaration_number"
        )

        # Checher "globex". Les deux compléments de l'entreprise Globex doivent être renvoyés
        results = get_search_results("Globex")
        self.assertEqual(len(results), 2)
        (self.assertIn(x.id, map(lambda x: x["id"], results)) for x in [fer, creatine])

        # Checher "omega". Seulement omega devrait sortir
        results = get_search_results("omega")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], omega.id)

        # Checher par ID (magnésium)
        results = get_search_results(magnesium.id)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], magnesium.id)

        # Chercher en ignorant les accents (magnésium)
        results = get_search_results("magnesium")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], magnesium.id)

        # Chercher par ID téléicare
        results = get_search_results("old_declaration_number")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], creatine.id)


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

        plant = PlantFactory()
        unknown_part = PlantPartFactory()
        self.assertFalse(plant.plant_parts.through.objects.filter(plantpart=unknown_part).exists())

        DeclaredPlantFactory(new=True, declaration=declaration)
        t = DeclaredPlantFactory(new=False, declaration=declaration, plant=plant, used_part=unknown_part)
        self.assertTrue(t.is_part_request, "vérifier que ce champ est bien assigné quand on utilise le factory")
        DeclaredSubstanceFactory(new=True, declaration=declaration)
        DeclaredMicroorganismFactory(new=True, declaration=declaration)
        DeclaredIngredientFactory(new=True, declaration=declaration)
        # n'envoie pas des ingrédients qui ne sont pas nouveaux et qui n'ont pas de nouvelles parties
        DeclaredPlantFactory(new=False, declaration=declaration)
        # n'envoie pas des ingrédients liés aux déclarations en brouillon
        DeclaredIngredientFactory(new=True, declaration=draft)

        response = self.client.get(reverse("api:list_new_declared_elements"), format="json")
        results = response.json()
        self.assertEqual(results["count"], 5)
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
    def test_filter_by_request_status(self):
        """
        La liste de demandes peut être filtrée par un ou plusieurs statuts de la demande
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        draft = DeclarationFactory(status=Declaration.DeclarationStatus.DRAFT)

        plant = DeclaredPlantFactory(new=True, declaration=declaration, request_status=Addable.AddableStatus.REQUESTED)
        DeclaredSubstanceFactory(new=True, declaration=declaration, request_status=Addable.AddableStatus.INFORMATION)
        DeclaredMicroorganismFactory(new=True, declaration=declaration, request_status=Addable.AddableStatus.REJECTED)
        ingredient = DeclaredIngredientFactory(
            new=False, declaration=declaration, request_status=Addable.AddableStatus.REPLACED
        )
        # n'envoie pas des ingrédients liés aux déclarations en brouillon
        DeclaredIngredientFactory(new=True, declaration=draft, request_status=Addable.AddableStatus.REQUESTED)

        filter_url = f"{reverse('api:list_new_declared_elements')}?requestStatus=REQUESTED,REPLACED"
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 2)
        returned_ids = [results["results"][0]["id"], results["results"][1]["id"]]
        self.assertIn(plant.id, returned_ids)
        self.assertIn(ingredient.id, returned_ids)

    @authenticate
    def test_filter_by_declaration_status(self):
        """
        La liste de demandes peut être filtrée par un ou plusieurs statuts de la déclaration
        """
        InstructionRoleFactory(user=authenticate.user)

        awaiting_instruction = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        observation = DeclarationFactory(status=Declaration.DeclarationStatus.OBSERVATION)
        draft = DeclarationFactory(status=Declaration.DeclarationStatus.DRAFT)
        authorized = DeclarationFactory(status=Declaration.DeclarationStatus.AUTHORIZED)

        plant_instruction = DeclaredPlantFactory(new=True, declaration=awaiting_instruction)
        microorganism_observation = DeclaredMicroorganismFactory(new=True, declaration=observation)
        ingredient_draft = DeclaredIngredientFactory(new=True, declaration=draft)
        DeclaredSubstanceFactory(new=True, declaration=authorized)

        filter_url = f"{reverse('api:list_new_declared_elements')}?declarationStatus=AWAITING_INSTRUCTION,OBSERVATION"
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 2)
        returned_ids = [results["results"][0]["id"], results["results"][1]["id"]]
        self.assertIn(plant_instruction.id, returned_ids)
        self.assertIn(microorganism_observation.id, returned_ids)

        filter_url = f"{reverse('api:list_new_declared_elements')}?declarationStatus=AWAITING_INSTRUCTION"
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 1)
        self.assertEqual(results["results"][0]["id"], plant_instruction.id)

        filter_url = f"{reverse('api:list_new_declared_elements')}?declarationStatus=OBSERVATION"
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 1)
        self.assertEqual(results["results"][0]["id"], microorganism_observation.id)

        # c'est possible de outrepasser l'exclusion de statuts fermés
        filter_url = f"{reverse('api:list_new_declared_elements')}?declarationStatus=DRAFT"
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 1)
        self.assertEqual(results["results"][0]["id"], ingredient_draft.id)

        # par défaut filtrer par statuts ouverts
        filter_url = f"{reverse('api:list_new_declared_elements')}?declarationStatus="
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 2)
        returned_ids = [results["results"][0]["id"], results["results"][1]["id"]]
        self.assertIn(plant_instruction.id, returned_ids)
        self.assertIn(microorganism_observation.id, returned_ids)

    @authenticate
    def test_filter_by_type(self):
        """
        Par défaut, on ne filtre pas par type. C'est possible de passer un ou plusieurs types pour filtrer les résultats.
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        DeclaredPlantFactory(new=True, declaration=declaration, new_name="My test plant")
        DeclaredMicroorganismFactory(new=True, declaration=declaration)
        DeclaredSubstanceFactory(new=True, declaration=declaration)
        DeclaredIngredientFactory(new=True, declaration=declaration)

        filter_url = f"{reverse('api:list_new_declared_elements')}?type=plant"
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 1)
        self.assertEqual(results["results"][0]["name"], "-NEW- My test plant")

        filter_url = f"{reverse('api:list_new_declared_elements')}?type=substance,microorganism,other-ingredient"
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 3)
        names = [result["name"] for result in results["results"]]
        self.assertNotIn("-NEW- My test plant", names)

        filter_url = f"{reverse('api:list_new_declared_elements')}?type="
        response = self.client.get(filter_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 4)

    @authenticate
    def test_filter_by_composition(self):
        """
        On peut filtrer par composition (utilisé dans la recherche avancée)
        """
        InstructionRoleFactory(user=authenticate.user)

        camomille = PlantFactory(name="Camomille")
        declaration_camomille = AwaitingInstructionDeclarationFactory()
        DeclaredPlantFactory(plant=camomille, declaration=declaration_camomille)

        eucalyptus = PlantFactory(name="Eucalyptus")
        declaration_eucalyptus = AwaitingInstructionDeclarationFactory()
        DeclaredPlantFactory(plant=eucalyptus, declaration=declaration_eucalyptus)

        lactobacilus = MicroorganismFactory(genus="Lactobacilus")
        declaration_lactobacilus = AwaitingInstructionDeclarationFactory()
        DeclaredMicroorganismFactory(microorganism=lactobacilus, declaration=declaration_lactobacilus)

        streptococcus = MicroorganismFactory(genus="Streptococcus")
        declaration_streptococcus = AwaitingInstructionDeclarationFactory()
        DeclaredMicroorganismFactory(microorganism=streptococcus, declaration=declaration_streptococcus)

        flavanones = SubstanceFactory(name="Flavanones")
        declaration_flavanones = AwaitingInstructionDeclarationFactory()
        ComputedSubstanceFactory(substance=flavanones, declaration=declaration_flavanones)

        levain = IngredientFactory(name="Levain")
        declaration_levain = AwaitingInstructionDeclarationFactory()
        DeclaredIngredientFactory(ingredient=levain, declaration=declaration_levain)

        declaration_both_plants = AwaitingInstructionDeclarationFactory()
        DeclaredPlantFactory(plant=camomille, declaration=declaration_both_plants)
        DeclaredPlantFactory(plant=eucalyptus, declaration=declaration_both_plants)

        declaration_both_microorganisms = AwaitingInstructionDeclarationFactory()
        DeclaredMicroorganismFactory(microorganism=lactobacilus, declaration=declaration_both_microorganisms)
        DeclaredMicroorganismFactory(microorganism=streptococcus, declaration=declaration_both_microorganisms)

        declaration_plant_mo = AwaitingInstructionDeclarationFactory()
        DeclaredPlantFactory(plant=camomille, declaration=declaration_plant_mo)
        DeclaredMicroorganismFactory(microorganism=lactobacilus, declaration=declaration_plant_mo)

        filter_url = f"{reverse('api:list_all_declarations')}?plants={camomille.id}"
        response = self.client.get(filter_url, format="json")
        body = response.json()
        self.assertEqual(body["count"], 3)
        self.assertIn(declaration_camomille.id, map(lambda x: x["id"], body["results"]))
        self.assertIn(declaration_both_plants.id, map(lambda x: x["id"], body["results"]))
        self.assertIn(declaration_plant_mo.id, map(lambda x: x["id"], body["results"]))

        filter_url = f"{reverse('api:list_all_declarations')}?plants={camomille.id},{eucalyptus.id}"
        response = self.client.get(filter_url, format="json")
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertIn(declaration_both_plants.id, map(lambda x: x["id"], body["results"]))

        filter_url = f"{reverse('api:list_all_declarations')}?microorganisms={lactobacilus.id}"
        response = self.client.get(filter_url, format="json")
        body = response.json()
        self.assertEqual(body["count"], 3)
        self.assertIn(declaration_lactobacilus.id, map(lambda x: x["id"], body["results"]))
        self.assertIn(declaration_both_microorganisms.id, map(lambda x: x["id"], body["results"]))
        self.assertIn(declaration_plant_mo.id, map(lambda x: x["id"], body["results"]))

        filter_url = f"{reverse('api:list_all_declarations')}?microorganisms={lactobacilus.id}&plants={camomille.id}"
        response = self.client.get(filter_url, format="json")
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertIn(declaration_plant_mo.id, map(lambda x: x["id"], body["results"]))

        filter_url = f"{reverse('api:list_all_declarations')}?substances={flavanones.id}"
        response = self.client.get(filter_url, format="json")
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertIn(declaration_flavanones.id, map(lambda x: x["id"], body["results"]))

        filter_url = f"{reverse('api:list_all_declarations')}?ingredients={levain.id}"
        response = self.client.get(filter_url, format="json")
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertIn(declaration_levain.id, map(lambda x: x["id"], body["results"]))

    @authenticate
    def test_order_by_creation_date(self):
        """
        C'est possible de trier par date de création
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

        plant = DeclaredPlantFactory(new=True, declaration=declaration_middle)
        microorganism = DeclaredMicroorganismFactory(new=True, declaration=declaration_first)
        ingredient = DeclaredIngredientFactory(new=True, declaration=declaration_last)

        order_url = f"{reverse('api:list_new_declared_elements')}?ordering=responseLimitDate"
        response = self.client.get(order_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 3)
        results = results["results"]
        self.assertEqual(results[0]["id"], ingredient.id)
        self.assertEqual(results[1]["id"], plant.id)
        self.assertEqual(results[2]["id"], microorganism.id)
        self.assertIn("responseLimitDate", results[0]["declaration"])

        order_url = f"{reverse('api:list_new_declared_elements')}?ordering=-responseLimitDate"
        response = self.client.get(order_url, format="json")
        results = response.json()
        self.assertEqual(results["count"], 3)
        results = results["results"]
        self.assertEqual(results[0]["id"], microorganism.id)
        self.assertEqual(results[1]["id"], plant.id)
        self.assertEqual(results[2]["id"], ingredient.id)


class TestSingleDeclaredElementApi(APITestCase):
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
            reverse("api:declared_element", kwargs={"pk": ingredient.id, "type": "other-ingredient"}), format="json"
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
            "Unknown type: 'unknown' not in ['plant', 'microorganism', 'substance', 'other-ingredient']",
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
            reverse("api:declared_element", kwargs={"pk": 1, "type": "other-ingredient"}), format="json"
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
            reverse("api:declared_element", kwargs={"pk": 1, "type": "other-ingredient"}), format="json"
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
            reverse("api:declared_element_request_info", kwargs={"pk": 1, "type": "other-ingredient"}), format="json"
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
            reverse("api:declared_element_reject", kwargs={"pk": 1, "type": "other-ingredient"}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_fields_hidden_from_declarant(self):
        """
        La déclaration ne doit pas contenir les champs statut et notes privés pour des ingrédients
        si l'user est un déclarant
        """
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)
        declaration = DeclarationFactory(author=authenticate.user, company=company)
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
        self.assertEqual(declared_plant.plant, plant)
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REPLACED)
        self.assertFalse(declared_plant.new)

    @authenticate
    def test_replace_inactive_ingredient_with_active(self):
        """
        Vérifier que c'est possible de remplacer un ingrédient par un autre
        Le front est responsable d'envoyer les bonnes valeurs pour `active`, `quantity`, `unit`
        selon la logique gérée là-bas
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_ingredient = DeclaredIngredientFactory(
            declaration=declaration,
            new=True,
            new_type=IngredientType.NON_ACTIVE_INGREDIENT.label,
            active=False,
            quantity=None,
            unit=None,
            ingredient=None,
        )
        self.assertNotEqual(declared_ingredient.request_status, DeclaredPlant.AddableStatus.REPLACED)
        active_ingredient = IngredientFactory(ingredient_type=IngredientType.ACTIVE_INGREDIENT)
        unit = UnitFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_ingredient.id, "type": "other-ingredient"}),
            {
                "element": {"id": active_ingredient.id, "type": "other-ingredient"},
                "additional_fields": {"active": True, "quantity": 20, "unit": unit.id},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        declared_ingredient.refresh_from_db()
        self.assertEqual(declared_ingredient.ingredient, active_ingredient)
        self.assertEqual(declared_ingredient.new_type, IngredientType.NON_ACTIVE_INGREDIENT.label)  # pas changé
        self.assertTrue(declared_ingredient.active)
        self.assertEqual(declared_ingredient.quantity, 20)
        self.assertEqual(declared_ingredient.unit, unit)
        self.assertEqual(declared_ingredient.request_status, DeclaredPlant.AddableStatus.REPLACED)
        self.assertFalse(declared_ingredient.new)

    @authenticate
    def test_can_replace_plant_request_with_microorganism(self):
        """
        Test de remplacement cross-type : plante vers microorganisme
        Verifier que les données sont copiées, et les nouvelles données sont sauvegardées.
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(
            declaration=declaration, new_name="Test plant", new_description="Test description", new=True, quantity=10
        )
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REQUESTED)
        microorganism = MicroorganismFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {
                "element": {"id": microorganism.id, "type": "microorganism"},
                "additional_fields": {
                    "strain": "Test strain",
                    "activated": False,
                    "quantity": 90,
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        with self.assertRaises(DeclaredPlant.DoesNotExist):
            DeclaredPlant.objects.get(id=declared_plant.id)

        self.assertEqual(DeclaredMicroorganism.objects.count(), 1)
        declared_microorganism = DeclaredMicroorganism.objects.get(declaration=declaration)

        self.assertEqual(declared_microorganism.microorganism, microorganism)
        self.assertEqual(declared_microorganism.request_status, DeclaredMicroorganism.AddableStatus.REPLACED)
        self.assertFalse(declared_microorganism.new)

        # est-ce que le nom est copié dans le champ espèce ?
        self.assertEqual(declared_microorganism.new_species, "Test plant")
        self.assertEqual(declared_microorganism.new_genre, "")
        # est-ce que les nouveaux champs sont sauvegardés ?
        self.assertEqual(declared_microorganism.strain, "Test strain")
        self.assertEqual(declared_microorganism.activated, False)
        self.assertEqual(declared_microorganism.quantity, 90)
        # est-ce que les anciens champs sont sauvegardés ?
        self.assertEqual(declared_microorganism.new_description, "Test description")

    @authenticate
    def test_can_replace_microorganism_request_with_plant(self):
        """
        Test de remplacement cross-type : microoganisme vers plante
        Verifier que les données sont copiées, et les nouvelles données sont sauvegardées.
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_microorganism = DeclaredMicroorganismFactory(
            declaration=declaration,
            new_species="test",
            new_genre="testing",
            new_description="Test description",
            new=True,
            quantity=10,
        )
        self.assertEqual(declared_microorganism.request_status, DeclaredMicroorganism.AddableStatus.REQUESTED)
        plant = PlantFactory()
        used_part = PlantPartFactory()
        unit = UnitFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_microorganism.id, "type": "microorganism"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "additional_fields": {
                    "used_part": used_part.id,
                    "unit": unit.id,
                    "quantity": 90,
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        with self.assertRaises(DeclaredMicroorganism.DoesNotExist):
            DeclaredMicroorganism.objects.get(id=declared_microorganism.id)

        self.assertEqual(DeclaredPlant.objects.count(), 1)
        declared_plant = DeclaredPlant.objects.get(declaration=declaration)

        self.assertEqual(declared_plant.plant, plant)
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REPLACED)
        self.assertFalse(declared_plant.new)

        # est-ce que l'espèce + genre sont copiés dans le champ nom ?
        self.assertEqual(declared_plant.new_name, "test testing")
        # est-ce que les nouveaux champs sont sauvegardés ?
        self.assertEqual(declared_plant.used_part, used_part)
        self.assertEqual(declared_plant.unit, unit)
        self.assertEqual(declared_plant.quantity, 90)
        # est-ce que les anciens champs sont sauvegardés ?
        self.assertEqual(declared_plant.new_description, "Test description")

    @authenticate
    def test_can_replace_substance_request_with_plant(self):
        """
        Test de remplacement cross-type : microoganisme vers plante
        Verifier que les données complexes, comme unit, sont bien gardées si elles ne sont pas spécifiées.
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        unit = UnitFactory()
        declared_substance = DeclaredSubstanceFactory(
            declaration=declaration, new_description="Test description", new=True, unit=unit
        )
        self.assertEqual(declared_substance.request_status, DeclaredSubstance.AddableStatus.REQUESTED)
        plant = PlantFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_substance.id, "type": "substance"}),
            {
                "element": {"id": plant.id, "type": "plant"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        with self.assertRaises(DeclaredSubstance.DoesNotExist):
            DeclaredSubstance.objects.get(id=declared_substance.id)

        self.assertEqual(DeclaredPlant.objects.count(), 1)
        declared_plant = DeclaredPlant.objects.get(declaration=declaration)

        self.assertEqual(declared_plant.plant, plant)
        self.assertEqual(declared_plant.request_status, DeclaredPlant.AddableStatus.REPLACED)
        self.assertFalse(declared_plant.new)

        # est-ce que les anciens champs sont sauvegardés ?
        self.assertEqual(declared_plant.new_description, "Test description")
        self.assertEqual(declared_plant.unit, unit)

    @authenticate
    def test_save_origin_declaration_on_replace(self):
        """
        Quand on remplace une demande par un ingrédient, si l'ingrédient a été créé dans la plateforme,
        on sauvegarde la declaration sur le fiche ingrédient pour suivre la raison de la création de l'ingrédient
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration)
        plant = PlantFactory(
            siccrf_id=None, origin_declaration=None
        )  # que les ingrédients créé via Compl'Alim ne vont pas avoir un siccrf_id

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {"element": {"id": plant.id, "type": "plant"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        plant.refresh_from_db()
        self.assertEqual(plant.origin_declaration, declaration)
        self.assertIsNone(plant.history.first().history_change_reason)

        # vérifier que la première déclaration est gardée quand l'ingrédient est réutilisé
        other_declaration = DeclarationFactory()
        other_declared_ingredient = DeclaredIngredientFactory(declaration=other_declaration)

        response = self.client.post(
            reverse(
                "api:declared_element_replace", kwargs={"pk": other_declared_ingredient.id, "type": "other-ingredient"}
            ),
            {"element": {"id": plant.id, "type": "plant"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        plant.refresh_from_db()
        self.assertEqual(
            plant.origin_declaration,
            declaration,
            "Quand l'ingrédient a déjà été utilisé, ne mets pas à jour la déclaration d'origine",
        )

    @authenticate
    def test_imported_ingredients_dont_get_origin_declaration(self):
        """
        Les ingrédients historiques doivent pas recevoir une déclaration d'origine
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration)
        plant = PlantFactory(siccrf_id=1234, origin_declaration=None)

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {"element": {"id": plant.id, "type": "plant"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        plant.refresh_from_db()
        self.assertIsNone(plant.origin_declaration)

    @authenticate
    def test_can_add_synonym_on_replace(self):
        """
        C'est possible d'envoyer une liste avec un element pour ajouter un synonyme
        et laisser des synonymes existantes non-modifiées
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration)
        plant = PlantFactory()
        synonym = PlantSynonymFactory.create(name="Eucalyptus Plant", standard_name=plant)

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "synonyms": [{"name": "New synonym"}],
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

    @authenticate
    def test_cannot_provide_synonym_with_no_name(self):
        """
        Si on donne un nom vide, ignore-le.
        Si on ne donne pas de nom, envoie un 400.
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration)
        plant = PlantFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "synonyms": [{"name": ""}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        plant.refresh_from_db()
        self.assertEqual(plant.plantsynonym_set.count(), 0)

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "synonyms": [{}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
        self.assertEqual(response.json()["globalError"], "Must provide 'name' to create new synonym")
        plant.refresh_from_db()
        self.assertEqual(plant.plantsynonym_set.count(), 0)

    @authenticate
    def test_cannot_add_duplicate_synonyms(self):
        """
        Ignorer les synonymes qui matchent des synonymes existantes
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration)
        plant = PlantFactory()
        synonym = PlantSynonymFactory.create(name="Eucalyptus Plant", standard_name=plant)

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_plant.id, "type": "plant"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "synonyms": [{"name": "Eucalyptus Plant"}, {"name": "New synonym"}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        plant.refresh_from_db()
        self.assertEqual(plant.plantsynonym_set.count(), 2)
        self.assertIsNotNone(plant.plantsynonym_set.get(name="New synonym"))
        self.assertEqual(plant.plantsynonym_set.get(id=synonym.id).name, synonym.name)

    @authenticate
    def test_elements_unchanged_on_replace_fail(self):
        """
        Si on donne des mauvaises données à sauvegarder, annule tout l'action, y compris la MAJ des synonymes
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_microorganism = DeclaredMicroorganismFactory(declaration=declaration)
        plant = PlantFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_microorganism.id, "type": "microorganism"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "additional_fields": {
                    "used_part": 99,  # fail: id unrecognised
                },
                "synonyms": [{"name": "New synonym"}],
            },
            format="json",
        )
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, body)
        self.assertEqual(
            body["fieldErrors"]["usedPart"][0], "Clé primaire «\xa099\xa0» non valide - l'objet n'existe pas.", body
        )
        # assertion implicite - l'objet existe tjs
        DeclaredMicroorganism.objects.get(id=declared_microorganism.id)
        self.assertFalse(plant.plantsynonym_set.filter(name="New synonym").exists())
        self.assertEqual(DeclaredPlant.objects.count(), 0)

    @authenticate
    def test_elements_unchanged_on_synonym_fail(self):
        """
        Si l'ajout de synonyme ne passe pas, on annule le remplacement complètement
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_microorganism = DeclaredMicroorganismFactory(declaration=declaration, quantity=10)
        plant = PlantFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_microorganism.id, "type": "microorganism"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "additional_fields": {
                    "quantity": 99,
                },
                "synonyms": [{}],
            },
            format="json",
        )
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, body)
        still_existing_declared_microorganism = DeclaredMicroorganism.objects.get(id=declared_microorganism.id)
        self.assertEqual(still_existing_declared_microorganism.quantity, 10)
        self.assertEqual(DeclaredPlant.objects.count(), 0)

    @authenticate
    def test_id_ignored_in_replace(self):
        """
        Vérifier que l'id d'un nouvel ingrédient déclaré est généré automatiquement, et non pas avec les données passées
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_microorganism = DeclaredMicroorganismFactory(id=66, declaration=declaration, new_species="test")
        self.assertEqual(declared_microorganism.id, 66)
        plant = PlantFactory()
        unit = UnitFactory()

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_microorganism.id, "type": "microorganism"}),
            {
                "element": {"id": plant.id, "type": "plant"},
                "additional_fields": {
                    "id": 99,
                    "unit": unit.id,
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        new_declared_plant = DeclaredPlant.objects.first()
        self.assertEqual(new_declared_plant.unit, unit)
        self.assertNotEqual(new_declared_plant.id, 66)
        self.assertNotEqual(new_declared_plant.id, 99)

    @authenticate
    def test_keep_article_16_on_replace_new_ingredient(self):
        """
        Vérifier que, avec la première utilisation d'un ingrédient créé, quand on remplace une demande
        avec cet ingrédient l'article de la déclaration reste en 16
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_microorganism = DeclaredMicroorganismFactory(declaration=declaration, new_species="test", new=True)
        declaration.assign_calculated_article()
        declaration.save()

        # on suppose que, avec les nouveaux ingrédients, la déclaration récoit un article 16
        declaration.refresh_from_db()
        self.assertEqual(declaration.calculated_article, Declaration.Article.ARTICLE_16)
        plant = PlantFactory(origin_declaration=None, siccrf_id=None)

        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_microorganism.id, "type": "microorganism"}),
            {"element": {"id": plant.id, "type": "plant"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        declaration.refresh_from_db()
        self.assertEqual(
            declaration.calculated_article,
            Declaration.Article.ARTICLE_16,
            "L'article reste en article 16 quand l'ingrédient a été créé au cause de cette demande",
        )

    @authenticate
    def test_get_article_15_on_replace_with_existing_ingredient(self):
        """
        Vérifier que l'article est recalculé avec un remplacement d'une demande
        L'article devrait changer que si la déclaration n'est pas l'origine de l'ingrédient
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory()
        declared_microorganism = DeclaredMicroorganismFactory(declaration=declaration, new_species="test", new=True)
        declaration.assign_calculated_article()
        declaration.save()

        # on suppose que, avec les nouveaux ingrédients, la déclaration récoit un article 16
        declaration.refresh_from_db()
        self.assertEqual(declaration.calculated_article, Declaration.Article.ARTICLE_16)

        existing_plant = PlantFactory(siccrf_id=None, origin_declaration=AuthorizedDeclarationFactory())
        response = self.client.post(
            reverse("api:declared_element_replace", kwargs={"pk": declared_microorganism.id, "type": "microorganism"}),
            {"element": {"id": existing_plant.id, "type": "plant"}},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        declaration.refresh_from_db()
        self.assertEqual(
            declaration.calculated_article,
            Declaration.Article.ARTICLE_15,
            "L'article devient article 15 quand l'ingrédient a été créé au cause de une autre demande",
        )

    @authenticate
    def test_part_created_on_accept_part(self):
        """
        Vérifier qu'une partie de plante est créée et autorisée quand on accepte une demande
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        plant = PlantFactory()
        unknown_part = PlantPartFactory()
        self.assertFalse(plant.plant_parts.through.objects.filter(plant=plant, plantpart=unknown_part).exists())

        declared_plant = DeclaredPlantFactory(new=False, declaration=declaration, plant=plant, used_part=unknown_part)

        response = self.client.post(
            reverse("api:declared_element_accept_part", kwargs={"pk": declared_plant.id, "type": "plant"}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        plant_part = plant.plant_parts.through.objects.get(plant=plant, plantpart=unknown_part)
        self.assertEqual(plant_part.status, IngredientStatus.AUTHORIZED)
        self.assertEqual(
            plant_part.history.first().history_change_reason,
            f"Ajoutée après une demande par la déclaration id : {declaration.id}",
        )
        declared_plant.refresh_from_db()
        self.assertEqual(declared_plant.request_status, Addable.AddableStatus.REPLACED)
        self.assertTrue(declared_plant.is_part_request)

    @authenticate
    def test_part_authorised_on_accept_part(self):
        """
        Vérifier qu'une partie de plante est autorisée quand on accepte une demande
        """
        InstructionRoleFactory(user=authenticate.user)

        declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        plant = PlantFactory()
        plant_part = PlantPartFactory()
        unauthorised_part = Part.objects.create(
            plant=plant, plantpart=plant_part, status=IngredientStatus.NOT_AUTHORIZED
        )

        declared_plant = DeclaredPlantFactory(new=False, declaration=declaration, plant=plant, used_part=plant_part)

        response = self.client.post(
            reverse("api:declared_element_accept_part", kwargs={"pk": declared_plant.id, "type": "plant"}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        unauthorised_part.refresh_from_db()
        self.assertEqual(unauthorised_part.status, IngredientStatus.AUTHORIZED)
        self.assertEqual(
            unauthorised_part.history.first().history_change_reason,
            f"Autorisée après une demande par la déclaration id : {declaration.id}",
        )
        declared_plant.refresh_from_db()
        self.assertEqual(declared_plant.request_status, Addable.AddableStatus.REPLACED)
        self.assertTrue(declared_plant.is_part_request)

    @authenticate
    @patch("config.tasks.recalculate_article_for_ongoing_declarations")
    def test_article_recalculated_on_accept_part(self, mocked_task):
        """
        Vérifier que l'article est recalculé avec une autorisation de partie de plante
        Quand c'est la première utilisation d'une partie, l'origin_declaration sera sauvegardé
        et la déclaration garde l'article 16. Les autres demandes pour la même partie seront remplacées
        et les déclarations recoivent l'article 15.
        Même comportement pour l'autorisation d'une partie.
        """
        InstructionRoleFactory(user=authenticate.user)

        first_declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        second_declaration = DeclarationFactory(status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        plant = PlantFactory()
        unknown_part = PlantPartFactory()
        self.assertFalse(plant.plant_parts.through.objects.filter(plantpart=unknown_part).exists())

        declared_plant = DeclaredPlantFactory(declaration=first_declaration, plant=plant, used_part=unknown_part)
        second_declared_plant = DeclaredPlantFactory(
            declaration=second_declaration, plant=plant, used_part=unknown_part
        )

        first_declaration.assign_calculated_article()
        first_declaration.save()
        second_declaration.assign_calculated_article()
        second_declaration.save()

        # on suppose que, avec les nouvelles parties de plantes, la déclaration récoit un article 16
        first_declaration.refresh_from_db()
        self.assertEqual(first_declaration.calculated_article, Declaration.Article.ARTICLE_16)

        response = self.client.post(
            reverse("api:declared_element_accept_part", kwargs={"pk": declared_plant.id, "type": "plant"}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        first_declaration.refresh_from_db()
        self.assertEqual(
            first_declaration.calculated_article,
            Declaration.Article.ARTICLE_16,
            "L'article reste en article 16 car la déclaration est la première utilisation",
        )

        # On lance le recalcul d'article pour d'autres déclarations
        mocked_task.assert_called_once()
        arguments = mocked_task.call_args.args
        queryset_argument = arguments[0]
        self.assertEqual(queryset_argument.count(), 1)
        self.assertTrue(queryset_argument.filter(id=second_declaration.id).exists())

        second_declared_plant.refresh_from_db()
        self.assertEqual(
            second_declared_plant.request_status,
            Addable.AddableStatus.REPLACED,
            "Statut MAJ pour d'autres demandes de la même partie",
        )
