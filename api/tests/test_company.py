from .utils import ProjectAPITestCase
from data.factories import CompanyFactory, CompanySupervisorFactory
from ..views.company import CompanyStatusChoices
from rest_framework import status


class TestCheckSiret(ProjectAPITestCase):
    viewname = "check_siret"

    def setUp(self):
        self.siret = "12345671234567"
        self.company = CompanyFactory(siret=self.siret)

    def test_check_siret_ok_unregistered_company(self):
        self.login()
        unexisting_siret = "99999999999999"
        response = self.get(self.url(siret=unexisting_siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.UNREGISTERED_COMPANY)

    def test_check_siret_ok_registered_and_supervised_by_me(self):
        me = self.login()
        CompanySupervisorFactory(user=me, companies=[self.company])
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME)

    def test_check_siret_ok_registered_and_supervised_by_other(self):
        self.login()
        CompanySupervisorFactory(companies=[self.company])
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER)

    def test_check_siret_ok_registered_and_unsupervised(self):
        self.login()
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED)

    def test_check_siret_ko_authenticated(self):
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
