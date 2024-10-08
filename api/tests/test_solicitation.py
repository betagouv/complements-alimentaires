from unittest import mock

from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    CollaborationInvitationFactory,
    CompanyAccessClaimFactory,
    CompanyFactory,
    SupervisorRoleFactory,
    UserFactory,
)

from .utils import ProjectAPITestCase


class TestListCollaborationInvitations(ProjectAPITestCase):
    viewname = "list_collaboration_invitation"

    @mock.patch("config.email.send_sib_template")
    def setUp(self, _):
        self.user = UserFactory()
        self.company_1 = CompanyFactory()
        self.company_2 = CompanyFactory()
        self.supervisor_role_1 = SupervisorRoleFactory(user=self.user, company=self.company_1)
        self.supervisor_role_2 = SupervisorRoleFactory(user=self.user, company=self.company_2)

        # solicitation déjà traitée (on la créé avant pour éviter une erreur d'intégrité à cause de la contrainte d'unicité)
        CollaborationInvitationFactory(recipient_email=self.user.email, company=self.company_1).account_created(
            processor=UserFactory()
        )

        self.solicitation_1 = CollaborationInvitationFactory(recipient_email=self.user.email, company=self.company_1)

        # solicitation liée au même utilisateur mais à une entreprise différente
        CollaborationInvitationFactory(recipient_email=self.user.email, company=self.company_2)

        # solicitation pas liée à l'utilisateur du tout
        self.company_3 = CompanyFactory()
        CollaborationInvitationFactory(company=self.company_3)

    def test_get_collaboration_invitations_ok(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.company_1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # seulement la solicitation 1

    def test_get_collaboration_invitations_ko_not_mine(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.company_3.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # get_or_404 appelé avant permission

    def test_get_collaboration_invitations_unauthenticated(self):
        response = self.get(self.url(pk=self.company_3.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCollaborationInvitationEmail(APITestCase):
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_account_created_sends_email(self, mocked_brevo):
        email = "test@example.com"
        company = CompanyFactory()
        sender = SupervisorRoleFactory(user=UserFactory(), company=company)

        invitation = CollaborationInvitationFactory(recipient_email=email, company=company, sender=sender.user)
        mocked_brevo.reset_mock()
        recipient = UserFactory(email=email)
        invitation.account_created(processor=recipient)

        template_number = 17
        mocked_brevo.assert_called_once_with(
            template_number,
            {
                "COMPANY_NAME": company.social_name,
                "NEW_COLLABORATOR": recipient.get_full_name(),
                "MEMBERS_LINK": f"https://hostname/gestion-des-collaborateurs/{company.id}",
            },
            sender.user.email,
            sender.user.get_full_name(),
        )


class TestListCompanyAccessClaims(ProjectAPITestCase):
    viewname = "list_company_access_claim"

    def setUp(self):
        self.user = UserFactory()
        self.company_1 = CompanyFactory()
        self.company_2 = CompanyFactory()
        self.supervisor_role_1 = SupervisorRoleFactory(user=self.user, company=self.company_1)
        self.supervisor_role_2 = SupervisorRoleFactory(user=self.user, company=self.company_2)

        self.solicitation_1 = CompanyAccessClaimFactory(recipients=[self.user], company=self.company_1)
        self.solicitation_2 = CompanyAccessClaimFactory(recipients=[self.user], company=self.company_1)

        # solicitation déjà traitée
        CompanyAccessClaimFactory(recipients=[self.user], company=self.company_1).accept(processor=self.user)

        # solicitation liée au même utilisateur mais à une entreprise différente
        CompanyAccessClaimFactory(recipients=[self.user], company=self.company_2)

        # solicitation pas liée à l'utilisateur du tout
        self.company_3 = CompanyFactory()
        CompanyAccessClaimFactory(company=self.company_3)

    def test_get_company_access_claims_ok(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.company_1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # seulement les solicitations 1 et 2

    def test_get_company_access_claims_ko_not_mine(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.company_3.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # get_or_404 appelé avant permission


class TestProcessCompanyAccessClaim(ProjectAPITestCase):
    viewname = "process_company_access_claim"

    def setUp(self):
        self.sender = UserFactory()
        self.recipent = UserFactory()
        self.company = CompanyFactory()
        SupervisorRoleFactory(user=self.recipent, company=self.company)
        self.solicitation = CompanyAccessClaimFactory(
            sender=self.sender, company=self.company, recipients=[self.recipent]
        )

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_process_company_access_claim_ok_with_accept(self, mocked_brevo):
        template_number = 13
        self.login(self.recipent)
        self.assertFalse(self.solicitation.processed_at)
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "accept"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mocked_brevo.assert_called_once_with(
            template_number,
            {
                "REQUESTER_NAME": self.sender.get_full_name(),
                "COMPANY_NAME": self.company.social_name,
                "DASHBOARD_LINK": f"https://hostname/tableau-de-bord?company={self.company.id}",
            },
            self.sender.email,
            self.sender.get_full_name(),
        )

        self.solicitation.refresh_from_db()
        self.assertTrue(self.solicitation.processed_at)
        self.assertEqual(self.solicitation.processor, self.recipent)
        self.assertEqual(self.solicitation.processed_action, "accept")
        self.assertTrue(self.sender in self.company.collaborators)

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    def test_process_company_access_claim_ok_with_refuse(self, mocked_brevo):
        template_number = 14
        self.login(self.recipent)
        self.assertFalse(self.solicitation.processed_at)
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "refuse"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mocked_brevo.assert_called_once_with(
            template_number,
            {
                "COMPANY_NAME": self.company.social_name,
            },
            self.sender.email,
            self.sender.get_full_name(),
        )

        self.solicitation.refresh_from_db()
        self.assertTrue(self.solicitation.processed_at)
        self.assertEqual(self.solicitation.processor, self.recipent)
        self.assertEqual(self.solicitation.processed_action, "refuse")
        self.assertFalse(self.sender in self.company.collaborators)

    def test_process_company_access_claim_ko_with_wrong_payload(self):
        self.login(self.recipent)
        for wrong_payload in [{}, {"action_name": "unexisting_action"}, {"wrong_field": ""}]:
            response = self.post(self.url(pk=self.solicitation.pk), wrong_payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_process_company_access_claim_ko_if_user_not_recipient(self):
        user_not_recipient = SupervisorRoleFactory(user=UserFactory(), company=self.company).user
        self.login(user_not_recipient)
        self.assertFalse(self.solicitation.processed_at)
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "accept"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_process_company_access_claim_ko_if_recipient_not_supervisor(self):
        # pourrait se produire si le gestionnaire perd ses droits entre la création et le traitement de la demande
        self.recipent.supervisable_companies.get(pk=self.company.pk).delete()
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "accept"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
