from rest_framework import status

from data.factories import (
    CollaborationInvitationFactory,
    CompanyFactory,
    CoSupervisionClaimFactory,
    SupervisorRoleFactory,
    UserFactory,
)

from .utils import ProjectAPITestCase


class TestListCollaborationInvitations(ProjectAPITestCase):
    viewname = "list_collaboration_invitation"

    def setUp(self):
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


class TestListCoSupervisionClaims(ProjectAPITestCase):
    viewname = "list_co_supervision_claim"

    def setUp(self):
        self.user = UserFactory()
        self.company_1 = CompanyFactory()
        self.company_2 = CompanyFactory()
        self.supervisor_role_1 = SupervisorRoleFactory(user=self.user, company=self.company_1)
        self.supervisor_role_2 = SupervisorRoleFactory(user=self.user, company=self.company_2)

        self.solicitation_1 = CoSupervisionClaimFactory(recipients=[self.user], company=self.company_1)
        self.solicitation_2 = CoSupervisionClaimFactory(recipients=[self.user], company=self.company_1)

        # solicitation déjà traitée
        CoSupervisionClaimFactory(recipients=[self.user], company=self.company_1).accept(processor=self.user)

        # solicitation liée au même utilisateur mais à une entreprise différente
        CoSupervisionClaimFactory(recipients=[self.user], company=self.company_2)

        # solicitation pas liée à l'utilisateur du tout
        self.company_3 = CompanyFactory()
        CoSupervisionClaimFactory(company=self.company_3)

    def test_get_co_supervision_claims_ok(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.company_1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # seulement les solicitations 1 et 2

    def test_get_co_supervision_claims_ko_not_mine(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.company_3.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # get_or_404 appelé avant permission


class TestProcessCoSupervisionClaim(ProjectAPITestCase):
    viewname = "process_co_supervision_claim"

    def setUp(self):
        self.sender = UserFactory()
        self.recipent = UserFactory()
        self.company = CompanyFactory()
        SupervisorRoleFactory(user=self.recipent, company=self.company)
        self.solicitation = CoSupervisionClaimFactory(
            sender=self.sender, company=self.company, recipients=[self.recipent]
        )

    def test_process_co_supervision_claim_ok_with_accept(self):
        self.login(self.recipent)
        self.assertFalse(self.solicitation.processed_at)
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "accept"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.solicitation.refresh_from_db()
        self.assertTrue(self.solicitation.processed_at)
        self.assertEqual(self.solicitation.processor, self.recipent)
        self.assertEqual(self.solicitation.processed_action, "accept")
        self.assertTrue(self.sender in self.company.collaborators)

    def test_process_co_supervision_claim_ok_with_refuse(self):
        self.login(self.recipent)
        self.assertFalse(self.solicitation.processed_at)
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "refuse"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.solicitation.refresh_from_db()
        self.assertTrue(self.solicitation.processed_at)
        self.assertEqual(self.solicitation.processor, self.recipent)
        self.assertEqual(self.solicitation.processed_action, "refuse")
        self.assertFalse(self.sender in self.company.collaborators)

    def test_process_co_supervision_claim_ko_with_wrong_payload(self):
        self.login(self.recipent)
        for wrong_payload in [{}, {"action_name": "unexisting_action"}, {"wrong_field": ""}]:
            response = self.post(self.url(pk=self.solicitation.pk), wrong_payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_process_co_supervision_claim_ko_if_user_not_recipient(self):
        user_not_recipient = SupervisorRoleFactory(user=UserFactory(), company=self.company).user
        self.login(user_not_recipient)
        self.assertFalse(self.solicitation.processed_at)
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "accept"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_process_co_supervision_claim_ko_if_recipient_not_supervisor(self):
        # pourrait se produire si le gestionnaire perd ses droits entre la création et le traitement de la demande
        self.recipent.supervisable_companies.get(pk=self.company.pk).delete()
        response = self.post(self.url(pk=self.solicitation.pk), {"action_name": "accept"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
