from unittest import mock

from django.test.utils import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CompanyFactory, UserFactory
from data.models import CompanyAccessClaim

from .utils import authenticate


class TestCompanyClaims(APITestCase):
    """
    Cette classe vise à tester les demandes d'accès aux entreprises
    """

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(SECURE=True)
    @override_settings(HOSTNAME="hostname")
    @mock.patch("config.email.send_sib_template")
    @authenticate
    def test_company_access_claim_declarant(self, mocked_brevo):
        """
        Un utilisateur peut demander accès déclarant à une entreprise
        """
        company = CompanyFactory()
        supervisor = UserFactory()
        company.supervisors.add(supervisor)
        template_number = 12

        payload = {
            "message": "Je voudrais pouvoir déclarer pour votre entreprise",
            "declarant_role": True,
            "supervisor_role": False,
        }
        response = self.client.post(
            reverse("api:claim_company_access", kwargs={"pk": company.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # On s'assure que l'email aux gestionnaires soit bien parti
        mocked_brevo.assert_called_once_with(
            template_number,
            {
                "REQUESTER_NAME": authenticate.user.get_full_name(),
                "COMPANY_NAME": company.social_name,
                "REQUEST_LINK": f"https://hostname/gestion-des-collaborateurs/{company.id}",
                "PERSONAL_MESSAGE": "Je voudrais pouvoir déclarer pour votre entreprise",
            },
            supervisor.email,
            supervisor.get_full_name(),
        )

        # On vérifie qu'on ait bien enregistré l'object CompanyAccessClaim dans la base
        claim = CompanyAccessClaim.objects.first()
        self.assertTrue(claim.declarant_role)
        self.assertFalse(claim.supervisor_role)
        self.assertEqual(claim.personal_msg, "Je voudrais pouvoir déclarer pour votre entreprise")
