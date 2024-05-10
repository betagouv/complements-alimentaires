from rest_framework import status

from data.factories import (
    CollaborationInvitationFactory,
    CompanyFactory,
    CoSupervisionClaimFactory,
    DeclarantRoleFactory,
    SupervisorRoleFactory,
    UserFactory,
)

from .utils import ProjectAPITestCase


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
        pass


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
