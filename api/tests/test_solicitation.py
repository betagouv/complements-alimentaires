from rest_framework import status

from data.factories.company import CompanyFactory, SupervisorRoleFactory
from data.factories.solicitation import CoSupervisionClaimFactory
from data.factories.user import UserFactory

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
        pass

    # Cas A : l'utilisateur n'existe pas en base, mais une invitation non traitée a déjà été envoyée
    # Cas B : l'utilisateur n'existe pas en base, et aucune invitation n'a été envoyée
    # Cas C : l'utilisateur existe en base et fait déjà partie des collaborateurs de l'entreprise
    # Cas D : l'utilisateur existe en base mais n'est pas encore collaborateur de l'entreprise
