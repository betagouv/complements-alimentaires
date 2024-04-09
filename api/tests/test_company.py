from .utils import ProjectAPITestCase
from data.factories import CompanyFactory, CompanySupervisorFactory
from ..views.company import CompanyStatusChoices
from data.models import Company
from rest_framework import status


class TestCheckSiret(ProjectAPITestCase):
    viewname = "check_company_siret"

    def setUp(self):
        self.siret = "12345671234567"
        self.company = CompanyFactory(siret=self.siret, social_name="Appeul")

    def test_check_company_siret_ok_unregistered_company(self):
        self.login()
        unexisting_siret = "99999999999999"
        response = self.get(self.url(siret=unexisting_siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.UNREGISTERED_COMPANY)
        self.assertIsNone(response.data["social_name"])

    def test_check_company_siret_ok_registered_and_supervised_by_me(self):
        me = self.login()
        CompanySupervisorFactory(user=me, companies=[self.company])
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME)
        self.assertEqual(response.data["social_name"], "Appeul")

    def test_check_company_siret_ok_registered_and_supervised_by_other(self):
        self.login()
        CompanySupervisorFactory(companies=[self.company])
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER)
        self.assertEqual(response.data["social_name"], "Appeul")

    def test_check_company_siret_ok_registered_and_unsupervised(self):
        self.login()
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_UNSUPERVISED)
        self.assertEqual(response.data["social_name"], "Appeul")

    def test_check_company_siret_ko_authenticated(self):
        response = self.get(self.url(siret=self.siret))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCreateCompany(ProjectAPITestCase):
    viewname = "company_create"

    def test_create_company_ok(self):
        self.login()
        company = CompanyFactory.build(social_name="Too Good To Leave")  # créé en mémoire, pas en DB
        companies_count = Company.objects.count()
        for key in ["_state", "id"]:
            company.__dict__.pop(key, None)
        response = self.post(self.url(), company.__dict__)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), companies_count + 1)

    def test_create_company_ko_missing_data(self):
        self.login()
        response = self.post(self.url(), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("address", response.data["field_errors"])

    def test_create_company_ko_unauthenticated(self):
        response = self.post(self.url(), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
