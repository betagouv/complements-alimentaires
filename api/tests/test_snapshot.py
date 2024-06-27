from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    DeclarantRoleFactory,
    InstructionReadyDeclarationFactory,
    InstructionRoleFactory,
    OngoingInstructionDeclarationFactory,
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

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, declarant_role.user)
        self.assertEqual(snapshot.comment, "Voici notre nouveau produit")

        # Si on sauvegarde une autre chose (pas le status) on ne devrait pas créer de snapshot
        declaration.name = "new name"
        declaration.save()
        self.assertEqual(declaration.snapshots.count(), 1)

    @authenticate
    def test_snapshot_creation_on_visa_request(self):
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        payload = {"comment": "J'objecte", "expiration": 45}
        response = self.client.post(
            reverse("api:object_with_visa", kwargs={"pk": declaration.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)

        # Dans le cas d'une requête de visa, les champs `commentaire` et
        # `expiration` ne sont pas marqués directement dans le snapshot, mais
        # sauvegardés dans le modèle pour les appliquer par la suite
        self.assertEqual(snapshot.comment, "")
        self.assertIsNone(snapshot.expiration_days)
        self.assertEqual(declaration.post_validation_producer_message, "J'objecte")
        self.assertEqual(declaration.post_validation_expiration_days, 45)

    @authenticate
    def test_snapshot_list_view(self):
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        payload = {"comment": "Voici notre nouveau produit"}
        self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), payload, format="json")
        declaration.refresh_from_db()
        snapshot = declaration.snapshots.first()

        # On obtient les snapshots liés à cette déclaration

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["id"], snapshot.id)
        self.assertEqual(body[0]["comment"], snapshot.comment)

    @authenticate
    def test_snapshot_list_view_unauthorized(self):
        declaration = InstructionReadyDeclarationFactory()

        # L'endpoint est seulement disponible pour l'auteur de la déclaration ou pour une
        # personne ayant le rôle d'instruction
        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        InstructionRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
