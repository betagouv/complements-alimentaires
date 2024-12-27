from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    CompanyFactory,
    DeclarantRoleFactory,
    InstructionReadyDeclarationFactory,
    InstructionRoleFactory,
    ObservationDeclarationFactory,
    OngoingInstructionDeclarationFactory,
    OngoingVisaDeclarationFactory,
    SnapshotFactory,
    SupervisorRoleFactory,
    VisaRoleFactory,
)
from data.models import Declaration, Snapshot

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
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.SUBMIT)
        self.assertEqual(snapshot.post_validation_status, "")

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
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)
        self.assertEqual(snapshot.post_validation_status, Declaration.DeclarationStatus.OBJECTION)

        # Dans le cas d'une requête de visa, les champs `commentaire` et
        # `expiration` ne sont pas marqués directement dans le snapshot, mais
        # sauvegardés dans le modèle pour les appliquer par la suite
        self.assertEqual(snapshot.comment, "")
        self.assertIsNone(snapshot.expiration_days)
        self.assertEqual(declaration.post_validation_producer_message, "J'objecte")
        self.assertEqual(declaration.post_validation_expiration_days, 45)
        self.assertEqual(declaration.post_validation_status, Declaration.DeclarationStatus.OBJECTION)

    @authenticate
    def test_snapshot_creation_on_observe(self):
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory(author=authenticate.user)

        payload = {"comment": "Ceci est une observation"}
        response = self.client.post(
            reverse("api:observe_no_visa", kwargs={"pk": declaration.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.comment, "Ceci est une observation")
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.OBSERVE_NO_VISA)
        self.assertEqual(snapshot.post_validation_status, "")

    @authenticate
    def test_snapshot_creation_on_authorize(self):
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory(author=authenticate.user)

        response = self.client.post(reverse("api:authorize_no_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.AUTHORIZE_NO_VISA)
        self.assertEqual(snapshot.post_validation_status, "")

    @authenticate
    def test_snapshot_creation_on_resubmit(self):
        company = CompanyFactory()
        declarant = DeclarantRoleFactory(user=authenticate.user, company=company)
        declaration = ObservationDeclarationFactory(author=declarant.user, company=company)

        response = self.client.post(reverse("api:resubmit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, declarant.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION)
        self.assertEqual(snapshot.post_validation_status, "")

    @authenticate
    def test_snapshot_creation_on_observe_with_visa(self):
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:observe_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)
        self.assertEqual(snapshot.post_validation_status, Declaration.DeclarationStatus.OBSERVATION)

    @authenticate
    def test_snapshot_creation_on_object_with_visa(self):
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:object_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)
        self.assertEqual(snapshot.post_validation_status, Declaration.DeclarationStatus.OBJECTION)

    @authenticate
    def test_snapshot_creation_on_reject_with_visa(self):
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:reject_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)
        self.assertEqual(snapshot.post_validation_status, Declaration.DeclarationStatus.REJECTED)

    @authenticate
    def test_snapshot_creation_on_authorize_with_visa(self):
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:authorize_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)
        self.assertEqual(snapshot.post_validation_status, Declaration.DeclarationStatus.AUTHORIZED)

    @authenticate
    def test_snapshot_creation_on_refuse_visa(self):
        instructor = VisaRoleFactory(user=authenticate.user)
        declaration = OngoingVisaDeclarationFactory()

        response = self.client.post(reverse("api:refuse_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.REFUSE_VISA)
        self.assertEqual(snapshot.post_validation_status, Declaration.DeclarationStatus.AUTHORIZED)

    @authenticate
    def test_snapshot_creation_on_accept_visa(self):
        instructor = VisaRoleFactory(user=authenticate.user)
        declaration = OngoingVisaDeclarationFactory()

        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Un snapshot devrait être créé
        declaration.refresh_from_db()
        self.assertEqual(declaration.snapshots.count(), 1)
        snapshot = declaration.snapshots.first()
        self.assertEqual(snapshot.declaration, declaration)
        self.assertEqual(snapshot.user, instructor.user)
        self.assertEqual(snapshot.action, Snapshot.SnapshotActions.ACCEPT_VISA)
        self.assertEqual(snapshot.post_validation_status, Declaration.DeclarationStatus.AUTHORIZED)

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
        """
        Une personne qui n'est pas lié à l'entreprise de la déclaration ne peut pas voir
        les snapshots
        """
        declaration = InstructionReadyDeclarationFactory()

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        InstructionRoleFactory(user=authenticate.user)
        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_snapshot_list_view_declaration_same_company(self):
        """
        Un user ayant le rôle de déclarant·e pour la même entreprise peut récupérer
        les snapshots
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        declaration = InstructionReadyDeclarationFactory(company=company)
        SnapshotFactory.create(declaration=declaration)

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_snapshot_list_view_supervision_same_company(self):
        """
        Un user ayant le rôle de supervision pour la même entreprise peut récupérer
        les snapshots
        """
        supervision_role = SupervisorRoleFactory(user=authenticate.user)
        company = supervision_role.company

        declaration = InstructionReadyDeclarationFactory(company=company)
        SnapshotFactory.create(declaration=declaration)

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_snapshot_list_view_declaration_mandated_company(self):
        """
        Un user ayant le rôle de déclaration pour l'entreprise mandatée peut recupérer
        les snapshots
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        declaration = InstructionReadyDeclarationFactory(mandated_company=company)
        SnapshotFactory.create(declaration=declaration)

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_snapshot_list_view_supervision_mandated_company(self):
        """
        Un user ayant le rôle de supervision pour l'entreprise mandatée peut recupérer
        les snapshots
        """
        supervision_role = SupervisorRoleFactory(user=authenticate.user)
        company = supervision_role.company

        declaration = InstructionReadyDeclarationFactory(mandated_company=company)
        SnapshotFactory.create(declaration=declaration)

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_snapshot_hide_visa_to_declarants(self):
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        snapshot = SnapshotFactory(
            declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.SUBMIT
        )
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REQUEST_VISA)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REFUSE_VISA)

        # On obtient les snapshots liés à cette déclaration. Cet user n'est pas viseur ni instructeur,
        # donc les snapshots liés à l'admin ne devraient pas s'afficher

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["id"], snapshot.id)
        self.assertEqual(body[0]["comment"], snapshot.comment)

    @authenticate
    def test_snapshot_show_visa_approval_to_declarants(self):
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        snapshot = SnapshotFactory(
            declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.SUBMIT
        )
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REQUEST_VISA)
        visa_accept_snapshot = SnapshotFactory(
            declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.ACCEPT_VISA
        )

        # On obtient les snapshots liés à cette déclaration. Cet user n'est pas viseur ni instructeur,
        # mais la validation du visa doit être communiqué

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["id"], snapshot.id)
        self.assertEqual(body[0]["comment"], snapshot.comment)

        self.assertEqual(body[1]["id"], visa_accept_snapshot.id)
        self.assertEqual(body[1]["comment"], visa_accept_snapshot.comment)

    @authenticate
    def test_snapshot_hide_visa_to_supervisors(self):
        supervision_role = SupervisorRoleFactory(user=authenticate.user)
        company = supervision_role.company

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(company=company)
        snapshot = SnapshotFactory(
            declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.SUBMIT
        )
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REQUEST_VISA)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REFUSE_VISA)

        # On obtient les snapshots liés à cette déclaration. Cet user n'est pas viseur ni instructeur,
        # donc les snapshots liés à l'admin ne devraient pas s'afficher

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["id"], snapshot.id)
        self.assertEqual(body[0]["comment"], snapshot.comment)

    @authenticate
    def test_snapshot_show_visa_to_visors(self):
        VisaRoleFactory(user=authenticate.user)

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.SUBMIT)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REQUEST_VISA)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REFUSE_VISA)

        # On obtient les snapshots liés à cette déclaration. Cet user n'est pas viseur ni instructeur,
        # donc les snapshots liés à l'admin ne devraient pas s'afficher

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 3)

    @authenticate
    def test_snapshot_show_visa_to_instructors(self):
        InstructionRoleFactory(user=authenticate.user)

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.SUBMIT)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REQUEST_VISA)
        SnapshotFactory(declaration=declaration, user=authenticate.user, action=Snapshot.SnapshotActions.REFUSE_VISA)

        # On obtient les snapshots liés à cette déclaration. Cet user n'est pas viseur ni instructeur,
        # donc les snapshots liés à l'admin ne devraient pas s'afficher

        response = self.client.get(reverse("api:declaration_snapshots", kwargs={"pk": declaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 3)
