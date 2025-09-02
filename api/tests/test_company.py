from unittest import mock

from django.test.utils import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from api.utils.urls import get_base_url
from data.factories import (
    CollaborationInvitationFactory,
    CompanyFactory,
    CompanyWithSiretFactory,
    CompanyWithVatFactory,
    DeclarantRoleFactory,
    InstructionRoleFactory,
    SupervisorRoleFactory,
    UserFactory,
)
from data.models import Company
from data.models.company import ActivityChoices

from ..views.company import CompanyStatusChoices
from .utils import ProjectAPITestCase, authenticate


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
    viewname = "company_retrieve_update"

    def setUp(self):
        self.company = CompanyFactory(social_name="Too Good")
        self.supervisor = SupervisorRoleFactory(company=self.company).user

    def test_retrieve_company_ok(self):
        self.login(self.supervisor)
        response = self.get(self.url(pk=self.company.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["social_name"], "Too Good")

    def test_retrieve_company_instructor_ok(self):
        instructor = InstructionRoleFactory()
        self.login(instructor.user)
        response = self.get(self.url(pk=self.company.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["social_name"], "Too Good")

    def test_retrieve_company_ko_unexising_company(self):
        self.login(self.supervisor)
        response = self.get(self.url(pk=99999999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_company_ko_not_a_supervisor(self):
        self.login()  # logged user is not a supervisor here
        response = self.get(self.url(pk=self.company.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_company_ko_unauthenticated(self):
        response = self.get(self.url(pk=self.company.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdateCompany(ProjectAPITestCase):
    viewname = "company_retrieve_update"

    def setUp(self):
        self.payload = dict(
            social_name="Too Good Corp",
            commercial_name="Too Good",
            siret="82073111500037",
            address="34 rue des peupliers",
            postal_code="75001",
            city="PARIS",
            country="FR",
            activities=[ActivityChoices.FABRICANT],
            phone_number="+33143324354",
            email="toogood@gmail.com",
        )

        self.company = CompanyFactory(**self.payload)
        self.supervisor = SupervisorRoleFactory(company=self.company).user

    def test_update_company_ok(self):
        self.login(self.supervisor)
        new_email = "toobad@gmail.com"
        self.payload["email"] = new_email
        response = self.put(self.url(pk=self.company.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.email, new_email)

    def test_update_company_ko_with_instructor(self):
        self.login(InstructionRoleFactory().user)
        response = self.put(self.url(pk=self.company.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_company_ko_unexising_company(self):
        self.login(self.supervisor)
        response = self.put(self.url(pk=99999999), self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_company_ko_unauthenticated(self):
        response = self.put(self.url(pk=self.company.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_company_ko_bad_data(self):
        self.login(self.supervisor)
        self.payload["phone_number"] = ""
        response = self.put(self.url(pk=self.company.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCreateCompany(ProjectAPITestCase):
    viewname = "company_create"

    def test_create_company_with_siret_ok(self):
        self.login()
        company = CompanyWithSiretFactory.build(social_name="Too Good To Leave")  # créé en mémoire, pas en DB
        companies_count = Company.objects.count()
        for key in [
            "_state",
            "creation_date",
            "modification_date",
            "id",
            "vat",
            "siccrf_id",
            "market_ready_count_cache",
            "market_ready_count_updated_at",
        ]:  # retire les champs à ne pas fournir dans le payload
            company.__dict__.pop(key, None)
        response = self.post(self.url(), company.__dict__)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), companies_count + 1)
        self.assertEqual(response.data["social_name"], "Too Good To Leave")

    def test_create_company_with_vat_ok(self):
        self.login()
        company = CompanyWithVatFactory.build(social_name="Too Bad To Join")  # créé en mémoire, pas en DB
        companies_count = Company.objects.count()
        for key in [
            "_state",
            "creation_date",
            "modification_date",
            "id",
            "siret",
            "siccrf_id",
            "market_ready_count_cache",
            "market_ready_count_updated_at",
        ]:  # retire les champs à ne pas fournir dans le payload
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

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_add_collaborator_without_account_but_invitation_already_sent_ko(self, mocked_brevo):
        self.login(self.adder)
        CollaborationInvitationFactory(recipient_email=self.recipient_email, company=self.company)
        mocked_brevo.reset_mock()

        # L'invité n'existe pas en base, mais une invitation non traitée a déjà été envoyée.
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test avec un-email qui une fois normalisé, devrait produire la même erreur
        response = self.post(
            self.url(pk=self.company.pk), dict(recipient_email="jean@EXAMPLE.com", roles=["DeclarantRole"])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        mocked_brevo.assert_not_called()

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_add_collaborator_without_account_ok(self, mocked_brevo):
        # L'invité n'existe pas en base, et aucune invitation n'a été envoyée
        self.login(self.adder)
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

        template_number = 16
        mocked_brevo.assert_called_once_with(
            template_number,
            {
                "COMPANY_NAME": self.company.social_name,
                "SENDER_NAME": self.adder.get_full_name(),
                "SIGNUP_LINK": f"https://hostname/inscription?email={self.recipient_email}",
            },
            self.recipient_email,
            self.recipient_email,
        )

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_add_collaborator_already_a_collaborator_ko(self, mocked_brevo):
        # L'invité existe en base et fait déjà partie des collaborateurs de l'entreprise.
        self.login(self.adder)
        DeclarantRoleFactory(user=UserFactory(email=self.recipient_email), company=self.company)
        response = self.post(self.url(pk=self.company.pk), self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        mocked_brevo.assert_not_called()

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_add_collaborator_with_account_ok(self, mocked_brevo):
        # L'invité existe en base mais n'est pas encore collaborateur de l'entreprise.
        self.login(self.adder)
        recipient = UserFactory()
        self.assertNotIn(recipient, self.company.collaborators)
        payload = dict(recipient_email=recipient.email, roles=["DeclarantRole"])
        response = self.post(self.url(pk=self.company.pk), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn(recipient, self.company.collaborators)

        template_number = 18
        mocked_brevo.assert_called_once_with(
            template_number,
            {
                "SENDER_NAME": self.adder.get_full_name(),
                "COMPANY_NAME": self.company.social_name,
                "DASHBOARD_LINK": f"https://hostname/tableau-de-bord?company={self.company.id}",
            },
            recipient.email,
            recipient.get_full_name(),
        )

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


class TestMandatedCompanies(APITestCase):
    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_add_mandated_company(self, mock):
        """
        Le gestionnaire d'une entreprise peut ajouter une autre entreprise en tant
        qu'entreprise mandatée. Un email doit être envoyé aux superviseurs de l'entreprise
        mandatée.
        """
        company = CompanyFactory()
        SupervisorRoleFactory(user=authenticate.user, company=company)

        mandated_company_1 = CompanyFactory()
        supervisor_1 = SupervisorRoleFactory(company=mandated_company_1)

        mandated_company_2 = CompanyFactory(vat="BE0582992566")
        supervisor_2 = SupervisorRoleFactory(company=mandated_company_2)

        url = reverse("api:add_mandated_company", kwargs={"pk": company.pk})

        # On peut utiliser le SIRET pour ajouter une compagnie
        response = self.client.post(url, {"siret": mandated_company_1.siret}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertIn(mandated_company_1, company.mandated_companies.all())

        brevo_template = 27
        mock.assert_called_once_with(
            brevo_template,
            {
                "COMPANY_NAME": company.social_name,
                "MANDATED_COMPANY_NAME": mandated_company_1.social_name,
                "DASHBOARD_LINK": f"{get_base_url()}tableau-de-bord?company={mandated_company_1.id}",
            },
            supervisor_1.user.email,
            supervisor_1.user.get_full_name(),
        )
        mock.reset_mock()

        # On peut aussi tester avec le numéro TVA
        response = self.client.post(url, {"vat": mandated_company_2.vat}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertIn(mandated_company_2, company.mandated_companies.all())

        mock.assert_called_once_with(
            27,
            {
                "COMPANY_NAME": company.social_name,
                "MANDATED_COMPANY_NAME": mandated_company_2.social_name,
                "DASHBOARD_LINK": f"{get_base_url()}tableau-de-bord?company={mandated_company_2.id}",
            },
            supervisor_2.user.email,
            supervisor_2.user.get_full_name(),
        )
        mock.reset_mock()

    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_add_mandated_company_not_found(self, mock):
        """
        Si l'entreprise mandatée ne se trove pas dans notre base de données l'API
        retourne un 404
        """
        company = CompanyFactory()
        SupervisorRoleFactory(user=authenticate.user, company=company)

        url = reverse("api:add_mandated_company", kwargs={"pk": company.pk})
        response = self.client.post(url, {"siret": "65257741834921"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        mock.assert_not_called()

    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_add_mandated_company_forbidden(self, mock):
        """
        L'utilisateur·ice doit avoir les droits de supervision pour l'entreprise
        souhaitant ajouter une entreprise mandatée
        """
        company = CompanyFactory()
        other_company = CompanyFactory()
        SupervisorRoleFactory(user=authenticate.user, company=company)

        url = reverse("api:add_mandated_company", kwargs={"pk": other_company.pk})
        response = self.client.post(url, {"siret": "65257741834921"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_add_mandated_company_declarant(self, mock):
        """
        Le rôle de déclarant·e ne permet pas d'ajouter une entreprise mandatée
        """
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)

        url = reverse("api:add_mandated_company", kwargs={"pk": company.pk})
        response = self.client.post(url, {"siret": "65257741834921"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        mock.assert_not_called()

    @mock.patch("config.email.send_sib_template")
    def test_add_mandated_company_unauthenticated(self, mock):
        """
        L'endpoint API n'est pas accessible sans authentifications
        """
        company = CompanyFactory()

        url = reverse("api:add_mandated_company", kwargs={"pk": company.pk})
        response = self.client.post(url, {"siret": "65257741834921"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        mock.assert_not_called()

    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_remove_mandated_company(self, mock):
        """
        Le gestionnaire d'une entreprise peut enlever une entreprise mandataire.
        """
        company = CompanyFactory()
        SupervisorRoleFactory(user=authenticate.user, company=company)

        mandated_company = CompanyFactory()
        company.mandated_companies.add(mandated_company)
        company.save()

        url = reverse("api:remove_mandated_company", kwargs={"pk": company.pk})

        response = self.client.post(url, {"id": mandated_company.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertNotIn(mandated_company, company.mandated_companies.all())

        mock.assert_not_called()

    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_remove_unexistent_company(self, mock):
        """
        Lors qu'on spécifie une entreprise non-mandatée la réponse est 200 et aucun
        changement s'effectue
        """
        company = CompanyFactory()
        SupervisorRoleFactory(user=authenticate.user, company=company)

        other_company = CompanyFactory()

        url = reverse("api:remove_mandated_company", kwargs={"pk": company.pk})

        response = self.client.post(url, {"id": other_company.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertNotIn(other_company, company.mandated_companies.all())

        mock.assert_not_called()

    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_remove_mandated_company_forbidden(self, mock):
        """
        L'utilisateur·ice doit avoir les droits de supervision pour l'entreprise
        souhaitant enlever une entreprise mandatée
        """
        company = CompanyFactory()
        other_company = CompanyFactory()
        SupervisorRoleFactory(user=authenticate.user, company=company)

        url = reverse("api:remove_mandated_company", kwargs={"pk": other_company.pk})
        response = self.client.post(url, {"id": other_company.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        mock.assert_not_called()

    @authenticate
    @mock.patch("config.email.send_sib_template")
    def test_remove_mandated_company_declarant(self, mock):
        """
        Le rôle déclarant·e ne suffit pas pour enlever une entreprise mandatée
        """
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)

        url = reverse("api:remove_mandated_company", kwargs={"pk": company.pk})
        response = self.client.post(url, {"id": company.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        mock.assert_not_called()

    @mock.patch("config.email.send_sib_template")
    def test_remove_mandated_company_unauthenticated(self, mock):
        """
        L'endpoint API n'est pas accessible sans authentifications
        """
        company = CompanyFactory()

        url = reverse("api:remove_mandated_company", kwargs={"pk": company.pk})
        response = self.client.post(url, {"id": company.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        mock.assert_not_called()
