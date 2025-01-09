from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import AwaitingInstructionDeclarationFactory, UserFactory


class RobotsTxtTests(TestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")

        assert response.status_code == HTTPStatus.OK
        assert response["content-type"] == "text/plain"
        assert response.content.startswith(b"User-Agent: *\n")

    def test_post_disallowed(self):
        response = self.client.post("/robots.txt")

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


class DeclarationPdfViewTests:
    """
    Cette class agit comme parente de `CertificateViewTests` et `SummaryViewTests`. Elle ne peut pas
    directement hériter d'APITestCase car on ne veut pas que le test-runner la prenne en compte.
    """

    view_name = None

    def setUp(self):
        self.user = UserFactory()
        self.declaration = AwaitingInstructionDeclarationFactory(author=self.user)

    def test_get_certificate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(self.view_name, kwargs={"pk": self.declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_forbidden(self):
        response = self.client.get(reverse(self.view_name, kwargs={"pk": self.declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_forbidden(self):
        response = self.client.get(reverse(self.view_name, kwargs={"pk": self.declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CertificateViewTests(DeclarationPdfViewTests, APITestCase):
    view_name = "web:certificate"


class SummaryViewTests(DeclarationPdfViewTests, APITestCase):
    view_name = "web:summary"
