from rest_framework import status

from data.factories import (
    CollaborationInvitationFactory,
    CompanyFactory,
    CompanyWithSiretFactory,
    CompanyWithVatFactory,
    DeclarantRoleFactory,
    SupervisorRoleFactory,
    UserFactory,
)
from data.models import Company

from ..views.company import CompanyStatusChoices
from .utils import ProjectAPITestCase


class TestCheckCompanyIdentifier(ProjectAPITestCase):
    viewname = "check_company_identifier"

    def setUp(self):
        self.siret = "80273782500611"  # SIRET luhn-valide
        self.company = CompanyFactory(siret=self.siret, social_name="Appeul")

        self.vat = "FR986745237856"
        self.company2 = CompanyFactory(vat=self.vat, social_name="Grosoft")

    def test_check_company_siret_ok_unregistered_company(self):
        self.login()
        unexisting_siret = "53786462100207"  # SIRET luhn-valide
        response = self.get(self.url(identifier=unexisting_siret) + "?identifierType=siret")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.UNREGISTERED_COMPANY)
        self.assertIsNone(response.data["company"])

    def test_check_company_vat_ok_unregistered_company(self):
        self.login()
        unexisting_vat = "DE999999999999"
        response = self.get(self.url(identifier=unexisting_vat) + "?identifierType=vat")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.UNREGISTERED_COMPANY)
        self.assertIsNone(response.data["company"])

    def test_check_company_siret_ok_registered_and_supervised_by_me(self):
        me = self.login()
        SupervisorRoleFactory(user=me, company=self.company)
        response = self.get(self.url(identifier=self.siret) + "?identifierType=siret")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME)
        self.assertEqual(response.data["company"]["social_name"], "Appeul")

    def test_check_company_vat_ok_registered_and_supervised_by_me(self):
        me = self.login()
        SupervisorRoleFactory(user=me, company=self.company2)
        response = self.get(self.url(identifier=self.vat) + "?identifierType=vat")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME)
        self.assertEqual(response.data["company"]["social_name"], "Grosoft")

    def test_check_company_siret_ok_registered_and_supervised_by_other(self):
        self.login()
        SupervisorRoleFactory(company=self.company)
        response = self.get(self.url(identifier=self.siret) + "?identifierType=siret")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER)
        self.assertEqual(response.data["company"]["social_name"], "Appeul")

    def test_check_company_vat_ok_registered_and_supervised_by_other(self):
        self.login()
        SupervisorRoleFactory(company=self.company2)
        response = self.get(self.url(identifier=self.vat) + "?identifierType=vat")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER)
        self.assertEqual(response.data["company"]["social_name"], "Grosoft")

    def test_check_company_siret_ok_registered_and_unsupervised(self):
        self.login()
        response = self.get(self.url(identifier=self.siret) + "?identifierType=siret")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED)
        self.assertEqual(response.data["company"]["social_name"], "Appeul")

    def test_check_company_vat_ok_registered_and_unsupervised(self):
        self.login()
        response = self.get(self.url(identifier=self.vat) + "?identifierType=vat")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED)
        self.assertEqual(response.data["company"]["social_name"], "Grosoft")

    def test_check_company_identifier_ko_unauthenticated(self):
        response = self.get(self.url(identifier=self.siret) + "?identifierType=siret")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_check_company_identifier_ko_with_wrong_identifier_type(self):
        self.login()
        response = self.get(self.url(identifier=self.siret) + "?identifierType=wrong")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRetrieveCompany(ProjectAPITestCase):
    viewname = "company_retrieve"

    def setUp(self):
        self.company = CompanyFactory(social_name="Too Good")
        self.supervisor = SupervisorRoleFactory(company=self.company)
        self.supervisor_user = self.supervisor.user

    def test_retrieve_company_ok(self):
        self.login(self.supervisor_user)
        response = self.get(self.url(pk=self.company.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["social_name"], "Too Good")

    def test_retrieve_ko_unexising_company(self):
        self.login(self.supervisor_user)
        response = self.get(self.url(pk=99999999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_ko_not_a_supervisor(self):
        self.login()  # logged user is not a supervisor here
        response = self.get(self.url(pk=self.company.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_ko_unauthenticated(self):
        response = self.get(self.url(pk=self.company.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCreateCompany(ProjectAPITestCase):
    viewname = "company_create"

    def test_create_company_with_siret_ok(self):
        self.login()
        company = CompanyWithSiretFactory.build(social_name="Too Good To Leave")  # créé en mémoire, pas en DB
        companies_count = Company.objects.count()
        for key in ["_state", "id", "vat"]:  # retire les champs à ne pas fournir dans le payload
            company.__dict__.pop(key, None)
        response = self.post(self.url(), company.__dict__)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), companies_count + 1)
        self.assertEqual(response.data["social_name"], "Too Good To Leave")

    def test_create_company_with_vat_ok(self):
        self.login()
        company = CompanyWithVatFactory.build(social_name="Too Bad To Join")  # créé en mémoire, pas en DB
        companies_count = Company.objects.count()
        for key in ["_state", "id", "siret"]:  # retire les champs à ne pas fournir dans le payload
            company.__dict__.pop(key, None)
        response = self.post(self.url(), company.__dict__)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), companies_count + 1)

    def test_create_company_ko_missing_data(self):
        self.login()
        response = self.post(self.url(), {"country": "FR"})  # si country non fourni, erreur liée à to_internal_value
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("address", response.data["field_errors"])

    def test_create_company_ko_unauthenticated(self):
        response = self.post(self.url(), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestGetCompanyCollaborators(ProjectAPITestCase):
    viewname = "get_company_collaborators"

    def setUp(self):
        self.company = CompanyFactory()

    def test_get_company_collaborators_ok(self):
        supervisor_role = SupervisorRoleFactory(company=self.company)
        DeclarantRoleFactory(company=self.company)
        self.login(supervisor_role.user)
        response = self.get(self.url(pk=self.company.pk))
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_company_collaborators_ko_unauthorized(self):
        self.login()
        response = self.get(self.url(pk=self.company.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestAddNewCollaborator(ProjectAPITestCase):
    viewname = "add_new_collaborator"

    def setUp(self):
        self.company = CompanyFactory()
        self.adder = UserFactory()  # "adder": la personne qui ajoute
        SupervisorRoleFactory(company=self.company, user=self.adder)

        self.recipient_email = "jean@example.com"
        self.payload = dict(recipient_email=self.recipient_email, roles=["DeclarantRole"])

    def test_add_collaborator_without_account_but_invitation_already_sent_ko(self):
        # L'invité n'existe pas en base, mais une invitation non traitée a déjà été envoyée.
        self.login(self.adder)
        CollaborationInvitationFactory(recipient_email=self.recipient_email, company=self.company)
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test avec un-email qui une fois normalisé, devrait produire la même erreur
        response = self.post(
            self.url(pk=self.company.pk), dict(recipient_email="jean@EXAMPLE.com", roles=["DeclarantRole"])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_collaborator_without_account_ok(self):
        # L'invité n'existe pas en base, et aucune invitation n'a été envoyée
        self.login(self.adder)
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_add_collaborator_already_a_collaborator_ko(self):
        # L'invité existe en base et fait déjà partie des collaborateurs de l'entreprise.
        self.login(self.adder)
        DeclarantRoleFactory(user=UserFactory(email=self.recipient_email), company=self.company)
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_collaborator_with_account_ok(self):
        # L'invité existe en base mais n'est pas encore collaborateur de l'entreprise.
        self.login(self.adder)
        recipient = UserFactory()
        self.assertNotIn(recipient, self.company.collaborators)
        payload = dict(recipient_email=recipient.email, roles=["DeclarantRole"])
        response = self.post(self.url(pk=self.company.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn(recipient, self.company.collaborators)

    def test_add_collaborator_not_logged_ko(self):
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_collaborator_without_supervisor_role_ko(self):
        adder = UserFactory()
        self.login(adder)
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Ajouter un rôle de gestionnaire mais à une autre entreprise ne doit rien changer
        SupervisorRoleFactory(user=adder, company=CompanyFactory())
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_collaborator_with_wrong_payload(self):
        self.login(self.adder)
        for wrong_payload in [
            dict(recipient_email="jean@example.com"),
            dict(roles=["DeclarantRole"]),
            dict(recipient_email=42, roles=["DeclarantRole"]),
            dict(recipient_email="valid_email@example.com", roles=["WrongRole"]),
        ]:
            response = self.post(self.url(pk=self.company.pk), wrong_payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
