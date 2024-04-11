from .utils import ProjectAPITestCase
from data.factories import (
    CompanyFactory,
    CompanyWithSiretFactory,
    CompanyWithVatFactory,
    CompanySupervisorFactory,
)
from ..views.company import CompanyStatusChoices
from data.models import Company
from rest_framework import status


class TestCheckCompanyIdentifier(ProjectAPITestCase):
    viewname = "check_company_identifier"

    def setUp(self):
        self.siret = "12345671234567"
        self.company = CompanyFactory(siret=self.siret, social_name="Appeul")

        self.vat = "FR986745237856"
        self.company2 = CompanyFactory(vat=self.vat, social_name="Grosoft")

    def test_check_company_siret_ok_unregistered_company(self):
        self.login()
        unexisting_siret = "99999999999999"
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
        CompanySupervisorFactory(user=me, companies=[self.company])
        response = self.get(self.url(identifier=self.siret) + "?identifierType=siret")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME)
        self.assertEqual(response.data["company"]["social_name"], "Appeul")

    def test_check_company_vat_ok_registered_and_supervised_by_me(self):
        me = self.login()
        CompanySupervisorFactory(user=me, companies=[self.company2])
        response = self.get(self.url(identifier=self.vat) + "?identifierType=vat")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_ME)
        self.assertEqual(response.data["company"]["social_name"], "Grosoft")

    def test_check_company_siret_ok_registered_and_supervised_by_other(self):
        self.login()
        CompanySupervisorFactory(companies=[self.company])
        response = self.get(self.url(identifier=self.siret) + "?identifierType=siret")
        self.assertEqual(response.data["company_status"], CompanyStatusChoices.REGISTERED_AND_SUPERVISED_BY_OTHER)
        self.assertEqual(response.data["company"]["social_name"], "Appeul")

    def test_check_company_vat_ok_registered_and_supervised_by_other(self):
        self.login()
        CompanySupervisorFactory(companies=[self.company2])
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
        self.supervisor = CompanySupervisorFactory(companies=[self.company])
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
        response = self.post(self.url(), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("address", response.data["field_errors"])

    def test_create_company_ko_unauthenticated(self):
        response = self.post(self.url(), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
