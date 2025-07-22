from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.choices import CountryChoices
from data.factories import CompanyFactory, ControlRoleFactory
from data.models import ActivityChoices

from .utils import authenticate


class TestCompanyControllers(APITestCase):
    @authenticate
    def test_get_list_not_allowed(self):
        """
        L'endpoint list_control_companies n'est pas accessible sans le rôle de contrôle
        """
        response = self.client.get(reverse("api:list_control_companies"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_unauthenticated(self):
        """
        L'endpoint list_control_companies n'est pas accessible sans être identifié·e
        """
        response = self.client.get(reverse("api:list_control_companies"), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_list_as_controller(self):
        """
        L'endpoint list_control_companies est diponible pour les personnes ayant le rôle de contrôle
        """
        ControlRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:list_control_companies"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_sort_by_name(self):
        """
        Il est possible de trier par nom de l'entreprise
        """
        ControlRoleFactory(user=authenticate.user)
        acme = CompanyFactory(social_name="Acme")
        dunder_mifflin = CompanyFactory(social_name="Dunder Mifflin")
        wonka = CompanyFactory(social_name="Wonka")

        response = self.client.get(reverse("api:list_control_companies") + "?ordering=+socialName", format="json")

        results = response.json()["results"]
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["id"], acme.id)
        self.assertEqual(results[1]["id"], dunder_mifflin.id)
        self.assertEqual(results[2]["id"], wonka.id)

        response = self.client.get(reverse("api:list_control_companies") + "?ordering=-socialName", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()["results"]

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["id"], wonka.id)
        self.assertEqual(results[1]["id"], dunder_mifflin.id)
        self.assertEqual(results[2]["id"], acme.id)

    @authenticate
    def test_retrieve_not_allowed(self):
        """
        L'endpoint retrieve_control_company n'est pas accessible sans le rôle de contrôle
        """
        company = CompanyFactory()
        response = self.client.get(reverse("api:retrieve_control_company", kwargs={"pk": company.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_unauthenticated(self):
        """
        L'endpoint retrieve_control_company n'est pas accessible sans être identifié·e
        """
        company = CompanyFactory()
        response = self.client.get(reverse("api:retrieve_control_company", kwargs={"pk": company.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_retrieve_as_controller(self):
        """
        L'endpoint retrieve_control_company est diponible pour les personnes ayant le rôle de contrôle
        """
        ControlRoleFactory(user=authenticate.user)
        company = CompanyFactory()
        response = self.client.get(reverse("api:retrieve_control_company", kwargs={"pk": company.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_filter_by_department(self):
        """
        Il est possible de filtrer par département
        """
        ControlRoleFactory(user=authenticate.user)
        acme = CompanyFactory(social_name="Acme", postal_code="69003", country=CountryChoices.FRANCE)
        dunder_mifflin = CompanyFactory(
            social_name="Dunder Mifflin", postal_code="69003", country=CountryChoices.AUSTRIA
        )
        wonka = CompanyFactory(social_name="Wonka", postal_code="98733", country=CountryChoices.FRANCE)
        monsters = CompanyFactory(social_name="Monsters Inc.", postal_code="20200", country=CountryChoices.FRANCE)

        # Entreprises étrangères
        response = self.client.get(reverse("api:list_control_companies") + "?departments=99", format="json")

        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], dunder_mifflin.id)

        # Entreprises dans le Rhône
        response = self.client.get(reverse("api:list_control_companies") + "?departments=69", format="json")

        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], acme.id)

        # Entreprises en Polynésie Française ou Haute-Corse
        response = self.client.get(reverse("api:list_control_companies") + "?departments=987,2B", format="json")

        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        self.assertCountEqual([r["id"] for r in results], [wonka.id, monsters.id])

        # Toutes les entreprises remontent si le filtre est vide
        response = self.client.get(reverse("api:list_control_companies") + "?departments=", format="json")

        results = response.json()["results"]
        self.assertEqual(len(results), 4)

    @authenticate
    def test_filter_by_activity(self):
        """
        Il est possible de filtrer par activité de l'entreprise
        """
        ControlRoleFactory(user=authenticate.user)
        acme = CompanyFactory(social_name="Acme", activities=[ActivityChoices.CONSEIL, ActivityChoices.DISTRIBUTEUR])
        dunder_mifflin = CompanyFactory(social_name="Dunder Mifflin", activities=[ActivityChoices.FABRICANT])
        wonka = CompanyFactory(social_name="Wonka", activities=[ActivityChoices.FAÇONNIER, ActivityChoices.FABRICANT])
        monsters = CompanyFactory(social_name="Monsters Inc.", activities=[ActivityChoices.INTRODUCTEUR])

        # Recherche par conseil
        response = self.client.get(reverse("api:list_control_companies") + "?activities=CONSEIL", format="json")

        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], acme.id)

        # Entreprises soit conseil, soit introductrices
        response = self.client.get(
            reverse("api:list_control_companies") + "?activities=CONSEIL,INTRODUCTEUR", format="json"
        )

        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        self.assertCountEqual([r["id"] for r in results], [acme.id, monsters.id])

        # Entreprises fabricantes
        response = self.client.get(reverse("api:list_control_companies") + "?activities=FABRICANT", format="json")

        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        self.assertCountEqual([r["id"] for r in results], [wonka.id, dunder_mifflin.id])
