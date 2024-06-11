from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    DeclarantRoleFactory,
    InstructionReadyDeclarationFactory,
)

from .utils import authenticate


class TestSnapshotApi(APITestCase):
    @authenticate
    def test_snapshot_creation_on_submit(self):
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        payload = {"comment": "Voici notre nouveau produit"}
        response = self.client.post(
            reverse("api:submit_declaration", kwargs={"pk": declaration.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # A snapshot should have been created
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, declarant_role.user)
        self.assertEqual(snapshot.comment, "Voici notre nouveau produit")
