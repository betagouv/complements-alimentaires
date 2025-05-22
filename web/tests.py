from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import AwaitingInstructionDeclarationFactory, UserFactory, SnapshotFactory
from data.models import Snapshot, Declaration

from web.views import CertificateView


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
        self.declaration.assign_calculated_article()
        self.declaration.save()

    def test_get_certificate(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(self.view_name, kwargs={"pk": self.declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_forbidden(self):
        response = self.client.get(reverse(self.view_name, kwargs={"pk": self.declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_forbidden(self):
        other_user = UserFactory()
        self.client.force_login(other_user)
        response = self.client.get(reverse(self.view_name, kwargs={"pk": self.declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CertificateViewTests(DeclarationPdfViewTests, APITestCase):
    view_name = "web:certificate"

    def test_get_certificate_with_submitted_article(self):
        """
        L'accusé d'enregistrement devrait montrer l'article qui a été assigné au moment de la dernière
        soumission et pas l'article actuel
        """
        SnapshotFactory(
            declaration=self.declaration,
            action=Snapshot.SnapshotActions.SUBMIT,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            json_declaration={"article": Declaration.Article.ARTICLE_16},
        )
        SnapshotFactory(
            declaration=self.declaration,
            action=Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            json_declaration={"article": Declaration.Article.ARTICLE_15},
        )
        self.declaration.overridden_article = Declaration.Article.ANSES_REFERAL
        self.declaration.save()
        self.declaration.refresh_from_db()
        self.assertEqual(self.declaration.article, Declaration.Article.ANSES_REFERAL)

        view = CertificateView()
        self.assertTrue(
            "art-15" in view.get_template_path(self.declaration),
            "On prend le template de l'article 15 même quand maintenant c'est different",
        )


class SummaryViewTests(DeclarationPdfViewTests, APITestCase):
    view_name = "web:summary"
