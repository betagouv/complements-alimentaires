"""
La logique dans ces tests peut sembler redondante (et elle l'est), mais :
1) c'est volontaire car le fait que les rôles déclarant et gestionnaire soient symétriques pourrait n'être que temporaire
2) c'est beaucoup moins impactant dans des tests que dans du code normal
"""

from rest_framework import status

from data.factories.company import CompanyFactory, DeclarantRoleFactory, SupervisorRoleFactory
from data.factories.user import UserFactory
from data.models import DeclarantRole, SupervisorRole

from ..serializers.user import CollaboratorSerializer
from .utils import ProjectAPITestCase


class TestAddDeclarantRole(ProjectAPITestCase):
    viewname = "add_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor_role = SupervisorRoleFactory(company=self.company)
        self.user = self.supervisor_role.user

        other_collaborator_role = SupervisorRoleFactory(company=self.company)
        self.collaborator = other_collaborator_role.user

        self.payload = dict(company_pk=self.company.pk, role_name="DeclarantRole")

    def test_add_declarant_role_ok(self):
        self.login(self.user)
        self.assertFalse(DeclarantRole.objects.filter(user=self.collaborator, company=self.company).exists())
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertTrue(DeclarantRole.objects.filter(user=self.collaborator, company=self.company).exists())

        # test de l'idempotence (ajouter un objet qui existe déjà ne provoque pas d'erreur)
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_declarant_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.post(self.url(user_pk=99999), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_declarant_role_non_employee_ko(self):
        self.login(self.user)
        user = UserFactory()
        response = self.post(self.url(user_pk=user.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_declarant_role_unexisting_company_ko(self):
        self.login(self.user)
        payload = dict(company_pk=99999, role_name="DeclarantRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_declarant_role_unauthenticated_ko(self):
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_declarant_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.collaborator.supervisable_companies.add(other_company)
        payload = dict(company_pk=other_company.pk, role_name="DeclarantRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRemoveDeclarantRole(ProjectAPITestCase):
    viewname = "remove_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = SupervisorRoleFactory(company=self.company)
        self.user = self.supervisor.user

        self.declarant_collaborator_role = DeclarantRoleFactory(company=self.company)
        self.collaborator = self.declarant_collaborator_role.user

        self.payload = dict(company_pk=self.company.pk, role_name="DeclarantRole")

    def test_remove_declarant_role_ok(self):
        self.login(self.user)
        self.assertTrue(DeclarantRole.objects.filter(user=self.collaborator, company=self.company).exists())
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertFalse(DeclarantRole.objects.filter(user=self.collaborator, company=self.company).exists())

        # test de la non idempotence (retirer un objet qui n'est plus n'est pas possible)
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.post(self.url(user_pk=99999), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unexisting_company_ko(self):
        self.login(self.user)
        payload = dict(company_pk=99999, role_name="DeclarantRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unauthenticated_ko(self):
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_declarant_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.collaborator.declarable_companies.add(other_company)
        payload = dict(company_pk=other_company.pk, role_name="DeclarantRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_declarant_role_to_not_collaborator_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.post(self.url(user_pk=not_collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_does_not_affect_role_in_other_company(self):
        self.login(self.user)
        other_company = CompanyFactory()
        self.collaborator.declarable_companies.add(other_company)
        self.assertEqual(self.collaborator.declarable_companies.count(), 2)
        self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(self.collaborator.declarable_companies.count(), 1)  # pas 0


class TestAddSupervisorRole(ProjectAPITestCase):
    viewname = "add_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = SupervisorRoleFactory(company=self.company)
        self.user = self.supervisor.user

        other_collaborator_role = DeclarantRoleFactory(company=self.company)
        self.collaborator = other_collaborator_role.user

        self.payload = dict(company_pk=self.company.pk, role_name="SupervisorRole")

    def test_add_supervisor_role_ok(self):
        self.login(self.user)
        self.assertFalse(SupervisorRole.objects.filter(user=self.collaborator, company=self.company).exists())
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertTrue(SupervisorRole.objects.filter(user=self.collaborator, company=self.company).exists())

        # test de l'idempotence (ajouter un objet qui existe déjà ne provoque pas d'erreur)
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_supervisor_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.post(self.url(user_pk=99999), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_supervisor_role_unexisting_company_ko(self):
        self.login(self.user)
        payload = dict(company_pk=99999, role_name="SupervisorRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_supervisor_role_unauthenticated_ko(self):
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_supervisor_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.collaborator.declarable_companies.add(other_company)
        payload = dict(company_pk=other_company.pk, role_name="SupervisorRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRemoveSupervisorRole(ProjectAPITestCase):
    viewname = "remove_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = SupervisorRoleFactory(company=self.company)
        self.user = self.supervisor.user

        self.supervisor_collaborator_role = SupervisorRoleFactory(company=self.company)
        self.collaborator = self.supervisor_collaborator_role.user

        # sugar
        self.payload = dict(company_pk=self.company.pk, role_name="SupervisorRole")

    def test_remove_supervisor_role_ok(self):
        self.login(self.user)
        self.assertTrue(SupervisorRole.objects.filter(user=self.collaborator, company=self.company).exists())
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertFalse(SupervisorRole.objects.filter(user=self.collaborator, company=self.company).exists())

        # test de la non idempotence (retirer un objet qui n'est plus n'est pas possible)
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.post(self.url(user_pk=99999), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_unexisting_company_ko(self):
        self.login(self.user)
        payload = dict(company_pk=99999, role_name="SupervisorRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_unauthenticated_ko(self):
        response = self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_supervisor_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.collaborator.declarable_companies.add(other_company)
        payload = dict(company_pk=other_company.pk, role_name="SupervisorRole")
        response = self.post(self.url(user_pk=self.collaborator.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_supervisor_role_to_not_collaborator_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.post(self.url(user_pk=not_collaborator.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_does_not_affect_role_in_other_company(self):
        self.login(self.user)
        other_company = CompanyFactory()
        self.collaborator.supervisable_companies.add(other_company)
        self.assertEqual(self.collaborator.supervisable_companies.count(), 2)
        self.post(self.url(user_pk=self.collaborator.pk), self.payload)
        self.assertEqual(self.collaborator.supervisable_companies.count(), 1)  # pas 0
