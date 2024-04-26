from rest_framework import status

from data.factories.company import CompanyFactory
from data.factories.roles import CompanySupervisorFactory, DeclarantFactory
from data.factories.user import UserFactory
from data.models.roles import Declarant

from ..serializers.user import StaffUserSerializer
from .utils import ProjectAPITestCase


class TestAddDeclarantRole(ProjectAPITestCase):
    viewname = "declarant_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = CompanySupervisorFactory(companies=[self.company])
        self.user = self.supervisor.user

        self.other_collaborator_role = CompanySupervisorFactory(companies=[self.company])
        self.collaborator = self.other_collaborator_role.user

    def test_add_declarant_role_ok(self):
        self.login(self.user)
        self.assertFalse(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, action="add"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, StaffUserSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertTrue(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())

        # test de l'idempotence (ajouter un objet qui existe déjà ne provoque pas d'erreur)
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, action="add"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_declarant_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=99999, action="add"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_declarant_role_unexisting_company_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=99999, collaborator_pk=self.collaborator.pk, action="add"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_declarant_role_unauthenticated_ko(self):
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, action="add"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_declarant_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.other_collaborator_role.companies.add(other_company)
        response = self.patch(
            self.url(company_pk=other_company.pk, collaborator_pk=self.collaborator.pk, action="add")
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_declarant_role_to_not_staff_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=not_collaborator.pk, action="add"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRemoveDeclarantRole(ProjectAPITestCase):
    viewname = "declarant_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = CompanySupervisorFactory(companies=[self.company])
        self.user = self.supervisor.user

        self.declarant_collaborator_role = DeclarantFactory(companies=[self.company])
        self.collaborator = self.declarant_collaborator_role.user

    def test_remove_declarant_role_ok(self):
        self.login(self.user)
        self.assertTrue(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, action="remove")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, StaffUserSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertFalse(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())

        # test de la non idempotence (retirer un objet qui n'est plus n'est pas possible)
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, action="remove")
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=99999, action="remove"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unexisting_company_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=99999, collaborator_pk=self.collaborator.pk, action="remove"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unauthenticated_ko(self):
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, action="remove")
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_declarant_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.declarant_collaborator_role.companies.add(other_company)
        response = self.patch(
            self.url(company_pk=other_company.pk, collaborator_pk=self.collaborator.pk, action="remove")
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_declarant_role_to_not_staff_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=not_collaborator.pk, action="remove")
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_does_not_affect_role_in_other_company(self):
        self.login(self.user)
        other_company = CompanyFactory()
        self.declarant_collaborator_role.companies.add(other_company)
        self.assertEqual(self.declarant_collaborator_role.companies.count(), 2)
        self.patch(self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, action="remove"))
        self.assertEqual(self.declarant_collaborator_role.companies.count(), 1)  # pas 0
