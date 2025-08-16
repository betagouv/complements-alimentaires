from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import AwaitingInstructionDeclarationFactory, CompanyFactory, ControlRoleFactory, SnapshotFactory
from data.models import Declaration, Snapshot

from .utils import authenticate


class TestDeclarationControllers(APITestCase):
    @authenticate
    def test_get_not_allowed(self):
        """
        L'endpoint n'est pas accessible sans le rôle de contrôle
        """
        response = self.client.get(reverse("api:list_control_declarations"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_unauthenticated(self):
        """
        L'endpoint n'est pas accessible sans être identifié·e
        """
        response = self.client.get(reverse("api:list_control_declarations"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_as_controller(self):
        """
        L'endpoint est diponible pour les personnes ayant le rôle de contrôle
        """
        ControlRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:list_control_declarations"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_sort_by_name(self):
        """
        Il est possible de trier par nom de produit
        """
        ControlRoleFactory(user=authenticate.user)
        vitamin_b12 = AwaitingInstructionDeclarationFactory(name="Vitamine B12")
        calcium = AwaitingInstructionDeclarationFactory(name="Calcium")
        magnesium = AwaitingInstructionDeclarationFactory(name="Magnesium")

        response = self.client.get(reverse("api:list_control_declarations") + "?ordering=+name", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["id"], calcium.id)
        self.assertEqual(results[1]["id"], magnesium.id)
        self.assertEqual(results[2]["id"], vitamin_b12.id)

        response = self.client.get(reverse("api:list_control_declarations") + "?ordering=-name", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["id"], vitamin_b12.id)
        self.assertEqual(results[1]["id"], magnesium.id)
        self.assertEqual(results[2]["id"], calcium.id)

    @authenticate
    def test_sort_by_company(self):
        """
        Il est possible de trier par nom de la compagnie
        """
        ControlRoleFactory(user=authenticate.user)

        acme = CompanyFactory(social_name="Acme")
        dunder_mifflin = CompanyFactory(social_name="Dunder Mifflin")
        wonka = CompanyFactory(social_name="Wonka")

        acme_declaration = AwaitingInstructionDeclarationFactory(name="Vitamine B12", company=acme)
        dunder_mifflin_declaration = AwaitingInstructionDeclarationFactory(name="Calcium", company=dunder_mifflin)
        wonka_declaration = AwaitingInstructionDeclarationFactory(name="Magnesium", company=wonka)

        response = self.client.get(reverse("api:list_control_declarations") + "?ordering=+companyName", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["id"], acme_declaration.id)
        self.assertEqual(results[1]["id"], dunder_mifflin_declaration.id)
        self.assertEqual(results[2]["id"], wonka_declaration.id)

        response = self.client.get(reverse("api:list_control_declarations") + "?ordering=-companyName", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["id"], wonka_declaration.id)
        self.assertEqual(results[1]["id"], dunder_mifflin_declaration.id)
        self.assertEqual(results[2]["id"], acme_declaration.id)

    @authenticate
    def test_simplified_status_article_15(self):
        """
        Les article 15 sont « Commercialisation possible » dès la soumission
        """
        ControlRoleFactory(user=authenticate.user)

        d1 = AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_15)
        SnapshotFactory(declaration=d1, action=Snapshot.SnapshotActions.SUBMIT)
        d2 = AwaitingInstructionDeclarationFactory(
            overridden_article=Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
        )
        SnapshotFactory(declaration=d2, action=Snapshot.SnapshotActions.SUBMIT)
        d3 = AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_15_WARNING)
        SnapshotFactory(declaration=d3, action=Snapshot.SnapshotActions.SUBMIT)

        response = self.client.get(reverse("api:list_control_declarations"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 3)

        for result in results:
            self.assertEqual(result["simplifiedStatus"], "Commercialisation possible")
            self.assertIsNotNone(result["simplifiedStatusDate"])

    @authenticate
    def test_simplified_status_other_articles(self):
        """
        Les autres articles sont en « Commercialisation possible » dès l'approbation
        """
        ControlRoleFactory(user=authenticate.user)

        AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_16)
        AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_18)

        response = self.client.get(reverse("api:list_control_declarations"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 2)

        for result in results:
            self.assertEqual(result["simplifiedStatus"], "En cours d'instruction")

    @authenticate
    def test_filter_by_simplified_status(self):
        """
        Il est possible de filtrer par le status simplifié
        """
        ControlRoleFactory(user=authenticate.user)

        ongoing_instruction_1 = AwaitingInstructionDeclarationFactory(
            overridden_article=Declaration.Article.ARTICLE_16
        )
        ongoing_instruction_2 = AwaitingInstructionDeclarationFactory(
            overridden_article=Declaration.Article.ARTICLE_18
        )
        ready_for_sale = AwaitingInstructionDeclarationFactory(
            overridden_article=Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
        )

        # Requête pour Commercialisation possible
        response = self.client.get(
            reverse("api:list_control_declarations") + "?simplifiedStatus=Commercialisation+possible", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], ready_for_sale.id)

        # Requête pour En cours d'instruction
        response = self.client.get(
            reverse("api:list_control_declarations") + "?simplifiedStatus=En+cours+d'instruction", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]

        self.assertEqual(len(results), 2)
        self.assertCountEqual([x["id"] for x in results], [ongoing_instruction_1.id, ongoing_instruction_2.id])

        # Requête pour tous les deux
        response = self.client.get(
            reverse("api:list_control_declarations")
            + "?simplified_status=Commercialisation+possible,En+cours+d'instruction",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 3)

    @authenticate
    def test_filter_by_surveillance_only(self):
        """
        Il est possible de filtrer par déclarations en statuts à surveiller
        """
        ControlRoleFactory(user=authenticate.user)

        # Déclarations à surveiller
        art_16 = AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_16)
        art_15_high_risk = AwaitingInstructionDeclarationFactory(
            overridden_article=Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
        )
        art_15_warning = AwaitingInstructionDeclarationFactory(
            overridden_article=Declaration.Article.ARTICLE_15_WARNING
        )

        # Déclarations sans risque
        AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_15)
        AwaitingInstructionDeclarationFactory(overridden_article=Declaration.Article.ARTICLE_18)

        # Requête pour toutes les déclarations
        response = self.client.get(reverse("api:list_control_declarations") + "?surveillanceOnly=false", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]
        self.assertEqual(len(results), 5)

        # Requête pour surveillanceOnly
        response = self.client.get(reverse("api:list_control_declarations") + "?surveillanceOnly=true", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]

        self.assertEqual(len(results), 3)
        self.assertCountEqual([x["id"] for x in results], [art_15_high_risk.id, art_15_warning.id, art_16.id])

    @authenticate
    def test_single_get_not_allowed(self):
        """
        L'endpoint pour une déclaration seule n'est pas accessible sans le rôle de contrôle
        """
        declaration = AwaitingInstructionDeclarationFactory()
        response = self.client.get(
            reverse("api:retrieve_control_declaration", kwargs={"pk": declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_single_get_unauthenticated(self):
        """
        L'endpoint pour une déclaration seule n'est pas accessible sans être identifié·e
        """
        declaration = AwaitingInstructionDeclarationFactory()
        response = self.client.get(
            reverse("api:retrieve_control_declaration", kwargs={"pk": declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_single_get_as_controller(self):
        """
        L'endpoint pour une déclaration seule est diponible pour les personnes ayant le rôle de contrôle
        """
        declaration = AwaitingInstructionDeclarationFactory()
        ControlRoleFactory(user=authenticate.user)
        response = self.client.get(
            reverse("api:retrieve_control_declaration", kwargs={"pk": declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_search_by_product_name(self):
        """
        Il est possible de rechercher par nom de produit
        """
        ControlRoleFactory(user=authenticate.user)
        shampoo = AwaitingInstructionDeclarationFactory(name="Super Shampoo")
        conditioner = AwaitingInstructionDeclarationFactory(name="Hair Conditioner")
        AwaitingInstructionDeclarationFactory(name="Hand Soap")

        # Match exact
        response = self.client.get(reverse("api:list_control_declarations") + "?search_name=Shampoo", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], shampoo.id)

        # Recherche partielle
        response = self.client.get(reverse("api:list_control_declarations") + "?search_name=Hair", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], conditioner.id)

        # Pas de résultat
        response = self.client.get(reverse("api:list_control_declarations") + "?search_name=Toothpaste", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 0)

    @authenticate
    def test_search_by_brand(self):
        """
        Il est possible de rechercher par marque
        """
        ControlRoleFactory(user=authenticate.user)
        loreal = AwaitingInstructionDeclarationFactory(brand="L'Oréal")
        garnier = AwaitingInstructionDeclarationFactory(brand="Garnier")
        AwaitingInstructionDeclarationFactory(brand="Dove")

        # Match exact
        response = self.client.get(reverse("api:list_control_declarations") + "?search_brand=Garnier", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], garnier.id)

        # Recherche partielle (case insensitive) - Au passage les accents ne sont pas
        # spécifiées, pourtant on obtient bien une réponse
        response = self.client.get(reverse("api:list_control_declarations") + "?search_brand=ore", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], loreal.id)

    @authenticate
    def test_search_by_company(self):
        """
        Il est possible de rechercher par entreprise
        """
        ControlRoleFactory(user=authenticate.user)
        company1 = CompanyFactory(social_name="Beauty Corp")
        company2 = CompanyFactory(social_name="Cosmetic Ltd")

        decl1 = AwaitingInstructionDeclarationFactory(company=company1)
        decl2 = AwaitingInstructionDeclarationFactory(company=company2)

        # Match exact
        response = self.client.get(
            reverse("api:list_control_declarations") + "?search_company=Cosmetic", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], decl2.id)

        # Recherche partielle
        response = self.client.get(reverse("api:list_control_declarations") + "?search_company=corp", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], decl1.id)
