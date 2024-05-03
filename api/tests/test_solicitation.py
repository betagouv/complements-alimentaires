from rest_framework import status

from data.factories.company import CompanyFactory, SupervisorRoleFactory
from data.factories.solicitation import RequestCoSupervisionFactory, RequestSupervisionFactory
from data.factories.user import UserFactory

from .utils import ProjectAPITestCase


class TestListUnprocessedSolicitations(ProjectAPITestCase):
    viewname = "list_solicitation"

    def setUp(self):
        self.user = UserFactory()
        self.company_1 = CompanyFactory()
        self.company_2 = CompanyFactory()
        self.supervisor_role_1 = SupervisorRoleFactory(user=self.user, company=self.company_1)
        self.supervisor_role_2 = SupervisorRoleFactory(user=self.user, company=self.company_2)

        self.solicitation_1 = RequestSupervisionFactory(recipients=[self.user], company=self.company_1)
        self.solicitation_2 = RequestCoSupervisionFactory(recipients=[self.user], company=self.company_1)

        # liée au même utilisateur mais à une entreprise différente
        self.solicitation_3 = RequestCoSupervisionFactory(recipients=[self.user], company=self.company_2)

        # cette fois pas liée à l'utilisateur du tout
        self.solicitation_4 = RequestCoSupervisionFactory()

    def test_get_unprocessed_solicitations_ok(self):
        self.login(self.user)
        response = self.get(self.url(pk=self.company_1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # seulement les solicitations 1 et 2
