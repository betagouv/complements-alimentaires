"""
La logique dans ces tests peut sembler redondante (et elle l'est), mais :
1) c'est volontaire car le fait que les rôles déclarant et gestionnaire soient symétriques pourrait n'être que temporaire
2) c'est beaucoup moins impactant dans des tests que dans du code normal
"""

from rest_framework import status

from data.factories.company import CompanyFactory
from data.factories.roles import DeclarantFactory, SupervisorFactory
from data.factories.user import UserFactory
from data.models.roles import Declarant, Supervisor

from ..serializers.user import CollaboratorSerializer
from .utils import ProjectAPITestCase


class TestAddDeclarantRole(ProjectAPITestCase):
    viewname = "company_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = SupervisorFactory(companies=[self.company])
        self.user = self.supervisor.user

        self.other_collaborator_role = SupervisorFactory(companies=[self.company])
        self.collaborator = self.other_collaborator_role.user

        # sugar
        self.kwargs = dict(role_class_name="Declarant", action="add")

    def test_add_declarant_role_ok(self):
        self.login(self.user)
        self.assertFalse(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertTrue(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())

        # test de l'idempotence (ajouter un objet qui existe déjà ne provoque pas d'erreur)
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_declarant_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=99999, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_declarant_role_unexisting_company_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=99999, collaborator_pk=self.collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_declarant_role_unauthenticated_ko(self):
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_declarant_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.other_collaborator_role.companies.add(other_company)
        response = self.patch(
            self.url(company_pk=other_company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_declarant_role_to_not_collaborator_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=not_collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRemoveDeclarantRole(ProjectAPITestCase):
    viewname = "company_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = SupervisorFactory(companies=[self.company])
        self.user = self.supervisor.user

        self.declarant_collaborator_role = DeclarantFactory(companies=[self.company])
        self.collaborator = self.declarant_collaborator_role.user

        # sugar
        self.kwargs = dict(role_class_name="Declarant", action="remove")

    def test_remove_declarant_role_ok(self):
        self.login(self.user)
        self.assertTrue(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertFalse(Declarant.objects.filter(user=self.collaborator, companies=self.company).exists())

        # test de la non idempotence (retirer un objet qui n'est plus n'est pas possible)
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=99999, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unexisting_company_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=99999, collaborator_pk=self.collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_unauthenticated_ko(self):
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_declarant_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.declarant_collaborator_role.companies.add(other_company)
        response = self.patch(
            self.url(company_pk=other_company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_declarant_role_to_not_collaborator_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=not_collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_declarant_role_does_not_affect_role_in_other_company(self):
        self.login(self.user)
        other_company = CompanyFactory()
        self.declarant_collaborator_role.companies.add(other_company)
        self.assertEqual(self.declarant_collaborator_role.companies.count(), 2)
        self.patch(self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs))
        self.assertEqual(self.declarant_collaborator_role.companies.count(), 1)  # pas 0


class TestAddSupervisorRole(ProjectAPITestCase):
    viewname = "company_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = SupervisorFactory(companies=[self.company])
        self.user = self.supervisor.user

        self.other_collaborator_role = DeclarantFactory(companies=[self.company])
        self.collaborator = self.other_collaborator_role.user

        # sugar
        self.kwargs = dict(role_class_name="Supervisor", action="add")

    def test_add_supervisor_role_ok(self):
        self.login(self.user)
        self.assertFalse(Supervisor.objects.filter(user=self.collaborator, companies=self.company).exists())
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertTrue(Supervisor.objects.filter(user=self.collaborator, companies=self.company).exists())

        # test de l'idempotence (ajouter un objet qui existe déjà ne provoque pas d'erreur)
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_supervisor_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=99999, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_supervisor_role_unexisting_company_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=99999, collaborator_pk=self.collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_supervisor_role_unauthenticated_ko(self):
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_supervisor_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.other_collaborator_role.companies.add(other_company)
        response = self.patch(
            self.url(company_pk=other_company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_supervisor_role_to_not_collaborator_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=not_collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestRemoveSupervisorRole(ProjectAPITestCase):
    viewname = "company_role"

    def setUp(self):
        self.company = CompanyFactory()
        self.supervisor = SupervisorFactory(companies=[self.company])
        self.user = self.supervisor.user

        self.supervisor_collaborator_role = SupervisorFactory(companies=[self.company])
        self.collaborator = self.supervisor_collaborator_role.user

        # sugar
        self.kwargs = dict(role_class_name="Supervisor", action="remove")

    def test_remove_supervisor_role_ok(self):
        self.login(self.user)
        self.assertTrue(Supervisor.objects.filter(user=self.collaborator, companies=self.company).exists())
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CollaboratorSerializer(self.collaborator, context={"company_id": self.company.pk}).data
        )
        self.assertFalse(Supervisor.objects.filter(user=self.collaborator, companies=self.company).exists())

        # test de la non idempotence (retirer un objet qui n'est plus n'est pas possible)
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_unexisting_user_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=99999, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_unexisting_company_ko(self):
        self.login(self.user)
        response = self.patch(self.url(company_pk=99999, collaborator_pk=self.collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_unauthenticated_ko(self):
        response = self.patch(
            self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_supervisor_role_to_unsupervised_company_ko(self):
        self.login(self.user)
        # On créé une autre entreprise dans laquelle le collaborateur a un rôle, mais notre utilisateur n'est pas gestionnaire
        other_company = CompanyFactory()
        self.supervisor_collaborator_role.companies.add(other_company)
        response = self.patch(
            self.url(company_pk=other_company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_supervisor_role_to_not_collaborator_user_ko(self):
        self.login(self.user)
        not_collaborator = UserFactory()
        response = self.patch(self.url(company_pk=self.company.pk, collaborator_pk=not_collaborator.pk, **self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_supervisor_role_does_not_affect_role_in_other_company(self):
        self.login(self.user)
        other_company = CompanyFactory()
        self.supervisor_collaborator_role.companies.add(other_company)
        self.assertEqual(self.supervisor_collaborator_role.companies.count(), 2)
        self.patch(self.url(company_pk=self.company.pk, collaborator_pk=self.collaborator.pk, **self.kwargs))
        self.assertEqual(self.supervisor_collaborator_role.companies.count(), 1)  # pas 0
