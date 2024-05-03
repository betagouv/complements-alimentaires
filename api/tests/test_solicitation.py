from rest_framework import status

from data.factories.solicitation import RequestCoSupervisionFactory, RequestSupervisionFactory
from data.factories.user import UserFactory

from .utils import ProjectAPITestCase


class TestListUnprocessedSolicitations(ProjectAPITestCase):
    viewname = "list_solicitation"

    def setUp(self):
        self.user = UserFactory()
        self.solicitation_1 = RequestSupervisionFactory(recipients=[self.user])
        self.solicitation_2 = RequestCoSupervisionFactory(recipients=[self.user])
        self.solicitation_3 = RequestCoSupervisionFactory()  # cette fois pas liée à l'utilisateur

    def test_get_unprocessed_solicitations_ok(self):
        self.login(self.user)
        response = self.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
