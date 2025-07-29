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
