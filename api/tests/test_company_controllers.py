from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CompanyFactory, ControlRoleFactory

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

    authenticate

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
