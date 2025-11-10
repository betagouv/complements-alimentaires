import datetime

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.choices import AuthorizationModes
from data.factories import (
    AttachmentFactory,
    AuthorizedDeclarationFactory,
    AwaitingInstructionDeclarationFactory,
    AwaitingVisaDeclarationFactory,
    CompanyFactory,
    DeclarantRoleFactory,
    InstructionReadyDeclarationFactory,
    InstructionRoleFactory,
    ObjectionDeclarationFactory,
    ObservationDeclarationFactory,
    OngoingInstructionDeclarationFactory,
    OngoingVisaDeclarationFactory,
    RejectedDeclarationFactory,
    VisaRoleFactory,
    WithdrawnDeclarationFactory,
)
from data.models import Attachment, Declaration, Snapshot

from .utils import authenticate


class TestDeclarationFlow(APITestCase):
    @authenticate
    def test_submit_declaration(self):
        """
        Passage du DRAFT -> AWAITING_INSTRUCTION
        Possible seulement si les données sont complètes
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        # Une déclaration avec toutes les conditions nécessaires pour l'instruction
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Si la pièce jointe pour l'étiquetage manque, on ne peut pas continuer
        missing_field_label = InstructionReadyDeclarationFactory(
            author=authenticate.user, company=company, attachments=[]
        )
        response = self.client.post(
            reverse("api:submit_declaration", kwargs={"pk": missing_field_label.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_errors = response.json()
        self.assertEqual(len(json_errors["fieldErrors"]), 1)
        self.assertIn("attachments", json_errors["fieldErrors"][0])

        # Si un champ obligatoire pour l'instruction manque, on le spécifie
        missing_field_declaration = InstructionReadyDeclarationFactory(
            author=authenticate.user, daily_recommended_dose="", company=company
        )
        response = self.client.post(
            reverse("api:submit_declaration", kwargs={"pk": missing_field_declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_errors = response.json()
        self.assertEqual(len(json_errors["fieldErrors"]), 1)
        self.assertIn("dailyRecommendedDose", json_errors["fieldErrors"][0])

        # S'il n'y a pas d'éléments dans la déclaration, on ne peut pas la soumettre pour instruction
        missing_elements_declaration = InstructionReadyDeclarationFactory(
            author=authenticate.user,
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            company=company,
        )
        response = self.client.post(
            reverse("api:submit_declaration", kwargs={"pk": missing_elements_declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_errors = response.json()
        self.assertEqual(len(json_errors["nonFieldErrors"]), 1)

        # NOTE: Si ce message d'erreur change, il faudra aussi changer StatusChangeErrorDisplay.vue dans
        # le frontend car il y a de la logique effectuée avec une comparaison de String
        self.assertEqual("Le complément doit comporter au moins un ingrédient", json_errors["nonFieldErrors"][0])

        # Si un des éléments de la composition manque des informations obligatoires, on ne peut pas soumettre
        # pour instruction
        missing_composition_data_declaration = InstructionReadyDeclarationFactory(
            author=authenticate.user,
            company=company,
        )
        first_declared_plant = missing_composition_data_declaration.declared_plants.first()
        first_declared_plant.used_part = None
        first_declared_plant.save()
        response = self.client.post(
            reverse("api:submit_declaration", kwargs={"pk": missing_composition_data_declaration.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json_errors = response.json()
        self.assertEqual(len(json_errors["nonFieldErrors"]), 1)

        # NOTE: Si ce message d'erreur change, il faudra aussi changer StatusChangeErrorDisplay.vue dans
        # le frontend car il y a de la logique effectuée avec une comparaison de String
        self.assertEqual(
            "Merci de renseigner les informations manquantes des plantes ajoutées", json_errors["nonFieldErrors"][0]
        )

    @authenticate
    def test_submit_declaration_eu_mode(self):
        """
        Passage du DRAFT -> AWAITING_INSTRUCTION
        En cas de nouvel ingrédient avec `authorization_mode == "EU"` on a besoin d'une
        pièce jointe non-étiquetage de plus ainsi que des informations sur le pays et
        la source reglémentaire.
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        plant = declaration.declared_plants.first()
        plant.new = True
        plant.authorization_mode = AuthorizationModes.EU
        plant.eu_reference_country = ""
        plant.save()

        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_errors = response.json()
        error_keys = [key for d in json_errors["fieldErrors"] for key in d]

        self.assertIn("attachments", error_keys)
        self.assertIn("euLegalSource", error_keys)
        self.assertIn("euReferenceCountry", error_keys)

        # On met les informations manquantes
        eu_proof = AttachmentFactory(type=Attachment.AttachmentType.REGULATORY_PROOF, declaration=declaration)
        eu_proof.save()

        plant.eu_reference_country = "DE"
        plant.eu_legal_source = "https://example.com/source"
        plant.save()

        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.SUBMIT)

    @authenticate
    def test_submit_declaration_no_auth_mode(self):
        """
        Passage du DRAFT -> AWAITING_INSTRUCTION
        En cas de nouvel ingrédient sans `authorization_mode` une erreur sera renvoyée
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company

        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)
        plant = declaration.declared_plants.first()
        plant.new = True
        plant.save()

        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        json_errors = response.json()
        error_keys = [key for d in json_errors["fieldErrors"] for key in d]
        self.assertIn("authorizationMode", error_keys)

        # On met les informations manquantes
        plant.authorization_mode = AuthorizationModes.FR
        plant.save()

        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.SUBMIT)

    @authenticate
    def test_submit_declaration_wrong_company(self):
        """
        Passage du DRAFT -> AWAITING_INSTRUCTION
        Ne devrait pas marcher si l'user n'est pas déclarant de l'entreprise
        """
        DeclarantRoleFactory(user=authenticate.user)
        wrong_company = CompanyFactory()

        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=wrong_company)
        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_submit_declaration_unauthenticated(self):
        """
        Passage du DRAFT -> AWAITING_INSTRUCTION
        Ne devrait pas marcher si on n'est pas authentifié.e
        """
        declaration = InstructionReadyDeclarationFactory()
        response = self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_take_declaration_for_instruction(self):
        """
        Passage du AWAITING_INSTRUCTION -> ONGOING_INSTRUCTION
        """
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = AwaitingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:take_for_instruction", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(instructor, declaration.instructor)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.TAKE_FOR_INSTRUCTION)

    @authenticate
    def test_take_declaration_unauthorized(self):
        """
        Passage du AWAITING_INSTRUCTION -> ONGOING_INSTRUCTION
        Seulement possible pour personnes ayant le rôle d'instructeur.ice
        """
        declaration = AwaitingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:take_for_instruction", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

    def test_take_declaration_unauthenticated(self):
        """
        Passage du AWAITING_INSTRUCTION -> ONGOING_INSTRUCTION
        Pas possible pour personnes non-authentifiées
        """
        declaration = AwaitingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:take_for_instruction", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

    @authenticate
    def test_take_declaration_for_visa(self):
        """
        Passage du AWAITING_VISA -> ONGOING_VISA
        """
        visor = VisaRoleFactory(user=authenticate.user)
        declaration = AwaitingVisaDeclarationFactory()

        response = self.client.post(reverse("api:take_for_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(visor, declaration.visor)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_VISA)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.TAKE_FOR_VISA)

    @authenticate
    def test_take_declaration_for_visa_unauthorized(self):
        """
        Passage du AWAITING_VISA -> ONGOING_VISA
        Seulement possible pour personnes ayant le rôle de visa
        """
        declaration = AwaitingVisaDeclarationFactory()

        response = self.client.post(reverse("api:take_for_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_VISA)

    def test_take_declaration_for_visa_unauthenticated(self):
        """
        Passage du AWAITING_VISA -> ONGOING_VISA
        Pas possible pour personnes non-authentifiées
        """
        declaration = AwaitingVisaDeclarationFactory()

        response = self.client.post(reverse("api:take_for_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_VISA)

    @authenticate
    def test_observe_declaration(self):
        """
        Passage du ONGOING_INSTRUCTION -> OBSERVATION
        """
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory(instructor=instructor)

        response = self.client.post(
            reverse("api:observe_no_visa", kwargs={"pk": declaration.id}),
            {"reasons": ["Forme assimilable à un aliment courant"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBSERVATION)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertIn("Forme assimilable à un aliment courant", latest_snapshot.blocking_reasons)
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.OBSERVE_NO_VISA)

    @authenticate
    def test_observe_someone_elses_declaration(self):
        """
        Passage du ONGOING_INSTRUCTION -> OBSERVATION lors qu'une autre instructrice
        que celle assignée fait l'opération
        """
        instructor = InstructionRoleFactory(user=authenticate.user)
        assigned_instructor = InstructionRoleFactory()
        declaration = OngoingInstructionDeclarationFactory(instructor=assigned_instructor)

        response = self.client.post(
            reverse("api:observe_no_visa", kwargs={"pk": declaration.id}),
            {"reasons": ["Forme assimilable à un aliment courant"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()

        # L'instructeur assigné a changé car c'est lui qui a fait la dernière action
        self.assertEqual(declaration.instructor, instructor)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(instructor.user, latest_snapshot.user)

    @authenticate
    def test_observe_declaration_unauthorized(self):
        """
        Passage du ONGOING_INSTRUCTION -> OBSERVATION
        Seulement possible pour personnes ayant le rôle d'instructeur.ice
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:observe_no_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def test_observe_declaration_unauthenticated(self):
        """
        Passage du ONGOING_INSTRUCTION -> OBSERVATION
        Pas possible pour personnes non-authentifiées
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:observe_no_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_authorize_declaration(self):
        """
        Passage du ONGOING_INSTRUCTION -> AUTHORIZED
        """
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory(instructor=instructor)

        response = self.client.post(reverse("api:authorize_no_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZED)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.AUTHORIZE_NO_VISA)

    @authenticate
    def test_authorize_declaration_unauthorized(self):
        """
        Passage du ONGOING_INSTRUCTION -> AUTHORIZED
        Seulement possible pour personnes ayant le rôle d'instructeur.ice
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:authorize_no_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def test_authorize_declaration_unauthenticated(self):
        """
        Passage du ONGOING_INSTRUCTION -> AUTHORIZED
        Pas possible pour personnes non-authentifiées
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:authorize_no_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_resubmit_declaration(self):
        """
        Passage du OBSERVATION -> AWAITING_INSTRUCTION
        """
        company = CompanyFactory()
        declarant = DeclarantRoleFactory(user=authenticate.user, company=company)
        declaration = ObservationDeclarationFactory(author=declarant.user, company=company)

        response = self.client.post(reverse("api:resubmit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION)

    @authenticate
    def test_resubmit_objection_declaration(self):
        """
        Passage du OBJECTION -> AWAITING_INSTRUCTION
        """
        company = CompanyFactory()
        declarant = DeclarantRoleFactory(user=authenticate.user, company=company)
        declaration = ObjectionDeclarationFactory(author=declarant.user, company=company)

        response = self.client.post(reverse("api:resubmit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.RESPOND_TO_OBJECTION)

    @authenticate
    def test_resubmit_declaration_unauthorized(self):
        """
        Passage du OBSERVATION -> AWAITING_INSTRUCTION
        Seulement possible pour l'auteur de la déclaration
        """
        declaration = ObservationDeclarationFactory()

        response = self.client.post(reverse("api:resubmit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBSERVATION)

    def test_resubmit_declaration_unauthenticated(self):
        """
        Passage du OBSERVATION -> AWAITING_INSTRUCTION
        Pas possible pour personnes non-authentifiées
        """
        declaration = ObservationDeclarationFactory()

        response = self.client.post(reverse("api:resubmit_declaration", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBSERVATION)

    @authenticate
    def test_observe_with_visa(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur OBSERVATION
        """
        InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(
            reverse("api:observe_with_visa", kwargs={"pk": declaration.id}),
            {"reasons": ["Forme assimilable à un aliment courant"]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.post_validation_status, Declaration.DeclarationStatus.OBSERVATION)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_VISA)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertIn("Forme assimilable à un aliment courant", latest_snapshot.blocking_reasons)
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)

    @authenticate
    def test_observe_with_visa_unauthorized(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur OBSERVATION
        Seulement possible pour personnes ayant le rôle d'instructeur.ice
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:observe_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def test_observe_with_visa_unauthenticated(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur OBSERVATION
        Pas possible pour personnes non-authentifiées
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:observe_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_object_with_visa(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur OBJECTION
        """
        InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:object_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.post_validation_status, Declaration.DeclarationStatus.OBJECTION)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_VISA)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)

    @authenticate
    def test_object_with_visa_unauthorized(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur OBJECTION
        Seulement possible pour personnes ayant le rôle d'instructeur.ice
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:object_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def test_object_with_visa_unauthenticated(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur OBJECTION
        Pas possible pour personnes non-authentifiées
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:object_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_reject_with_visa(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur REJECT
        """
        InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:reject_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.post_validation_status, Declaration.DeclarationStatus.REJECTED)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_VISA)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)

    @authenticate
    def test_reject_with_visa_unauthorized(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur REJECT
        Seulement possible pour personnes ayant le rôle d'instructeur.ice
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:reject_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def test_reject_with_visa_unauthenticated(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur REJECT
        Pas possible pour personnes non-authentifiées
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:reject_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_authorize_with_visa(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur AUTHORIZE
        """
        InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:authorize_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.post_validation_status, Declaration.DeclarationStatus.AUTHORIZED)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_VISA)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.REQUEST_VISA)

    @authenticate
    def test_authorize_with_visa_unauthorized(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur AUTHORIZE
        Seulement possible pour personnes ayant le rôle d'instructeur.ice
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:authorize_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def test_authorize_with_visa_unauthenticated(self):
        """
        Passage de ONGOING_INSTRUCTION à AWAITING_VISA en abboutissant sur AUTHORIZE
        Pas possible pour personnes non-authentifiées
        """
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:authorize_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_refuse_visa(self):
        """
        Passage de ONGOING_VISA à AWAITING_INSTRUCTION
        """
        VisaRoleFactory(user=authenticate.user)
        declaration = OngoingVisaDeclarationFactory()

        response = self.client.post(reverse("api:refuse_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.post_validation_status, "")
        self.assertEqual(declaration.post_validation_producer_message, "")
        self.assertEqual(declaration.post_validation_expiration_days, None)

        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.REFUSE_VISA)

    @authenticate
    def refuse_visa_unauthorized(self):
        """
        Passage de ONGOING_VISA à AWAITING_INSTRUCTION
        Seulement possible pour personnes ayant le rôle de visur·se
        """
        declaration = OngoingVisaDeclarationFactory()

        response = self.client.post(reverse("api:refuse_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def refuse_visa_unauthenticated(self):
        """
        Passage de ONGOING_VISA à AWAITING_INSTRUCTION
        Pas possible pour les personnes non-authentifiées
        """
        declaration = OngoingVisaDeclarationFactory()

        response = self.client.post(reverse("api:refuse_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_accept_visa(self):
        """
        Passage de ONGOING_VISA à { AUTHORIZED | REJECTED | OBJECTION | OBSERVATION }
        """
        VisaRoleFactory(user=authenticate.user)

        # AUTHORIZED
        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.AUTHORIZED,
            post_validation_producer_message="À authoriser",
            post_validation_expiration_days=12,
        )

        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZED)

        # Il n'y a pas de commentaires pour une autorisation, même si le post_validation_producer_message
        # est rempli
        self.assertEqual(latest_snapshot.comment, "")

        # Il n'y a pas d'expiration_days pour une autorisation même si post_validation_expiration_days est rempli
        self.assertIsNone(latest_snapshot.expiration_days)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.ACCEPT_VISA)

        # REJECTED
        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.REJECTED,
            post_validation_producer_message="À refuser",
            post_validation_expiration_days=20,
        )

        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")

        declaration.refresh_from_db()
        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.REJECTED)
        self.assertEqual(latest_snapshot.comment, "À refuser")
        self.assertEqual(latest_snapshot.expiration_days, 20)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.ACCEPT_VISA)

        # OBJECTION
        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.OBJECTION,
            post_validation_producer_message="Objection",
            post_validation_expiration_days=22,
        )

        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")

        declaration.refresh_from_db()
        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBJECTION)
        self.assertEqual(latest_snapshot.comment, "Objection")
        self.assertEqual(latest_snapshot.expiration_days, 22)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.ACCEPT_VISA)

        # OBSERVATION
        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.OBSERVATION,
            post_validation_producer_message="Observation",
            post_validation_expiration_days=23,
        )

        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")

        declaration.refresh_from_db()
        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBSERVATION)
        self.assertEqual(latest_snapshot.comment, "Observation")
        self.assertEqual(latest_snapshot.expiration_days, 23)

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.ACCEPT_VISA)

    @authenticate
    def test_visor_can_modify_decision(self):
        """
        La viseuse peut modifier la décision de l'instructrice
        """
        VisaRoleFactory(user=authenticate.user)

        # L'instructrice à marqué cette déclaration comme « autorisée », mais la viseuse la fera
        # passer en observation
        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.AUTHORIZED,
            post_validation_producer_message="À authoriser",
        )

        body = {
            "comment": "overridden comment",
            "proposal": "OBSERVATION",
            "delayDays": 6,
            "reasons": [
                "a",
                "b",
            ],
        }
        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), body, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBSERVATION)
        self.assertEqual(latest_snapshot.comment, "overridden comment")
        self.assertEqual(latest_snapshot.status, Declaration.DeclarationStatus.OBSERVATION)
        self.assertEqual(latest_snapshot.expiration_days, 6)
        self.assertEqual(latest_snapshot.blocking_reasons, ["a", "b"])

        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.ACCEPT_VISA)

    @authenticate
    def test_visor_cant_modify_on_refuse(self):
        """
        Refuser un visa n'applique pas les modifications
        """
        VisaRoleFactory(user=authenticate.user)

        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.AUTHORIZED,
            post_validation_producer_message="À authoriser",
        )

        body = {
            "comment": "overridden comment",
            "proposal": "OBSERVATION",
            "delayDays": 6,
            "reasons": [
                "a",
                "b",
            ],
        }
        response = self.client.post(reverse("api:refuse_visa", kwargs={"pk": declaration.id}), body, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        self.assertEqual(latest_snapshot.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        self.assertEqual(latest_snapshot.comment, "")
        self.assertEqual(latest_snapshot.expiration_days, None)
        self.assertEqual(latest_snapshot.blocking_reasons, None)

    @authenticate
    def accept_visa_unauthorized(self):
        """
        Passage de ONGOING_VISA à à { AUTHORIZED | REJECTED | OBJECTION | OBSERVATION }
        Seulement possible pour personnes ayant le rôle de visur·se
        """
        declaration = OngoingVisaDeclarationFactory()

        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    def accept_visa_unauthenticated(self):
        """
        Passage de ONGOING_VISA à à { AUTHORIZED | REJECTED | OBJECTION | OBSERVATION }
        Pas possible pour les personnes non-authentifiées
        """
        declaration = OngoingVisaDeclarationFactory()

        response = self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)

    @authenticate
    def test_withdraw(self):
        """
        Passage de AUTHORIZED à WITHDRAWN
        Seulement possible pour les déclarant·e·s de la déclaration en question
        """
        declaration = AuthorizedDeclarationFactory(author=authenticate.user)

        payload = {"effective_withdrawal_date": "2026-05-08"}
        response = self.client.post(reverse("api:withdraw", kwargs={"pk": declaration.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        declaration.refresh_from_db()
        latest_snapshot = declaration.snapshots.latest("creation_date")
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.WITHDRAWN)
        self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.WITHDRAW)
        self.assertEqual(latest_snapshot.effective_withdrawal_date, datetime.date(2026, 5, 8))

        declaration = AuthorizedDeclarationFactory()
        VisaRoleFactory(user=authenticate.user)

        response = self.client.post(reverse("api:withdraw", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZED)

        declaration = AuthorizedDeclarationFactory()
        InstructionRoleFactory(user=authenticate.user)

        response = self.client.post(reverse("api:withdraw", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZED)

    def test_withdraw_unauthoritzed(self):
        """
        Passage de AUTHORIZED à WITHDRAWN
        Pas possible si la personne n'est pas autrice de la déclaration en question
        """
        declaration = AuthorizedDeclarationFactory()

        response = self.client.post(reverse("api:withdraw", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZED)

    def test_withdraw_unauthenticated(self):
        """
        Passage de AUTHORIZED à WITHDRAWN
        Pas possible pour les personnes non-authentifiées
        """
        declaration = AuthorizedDeclarationFactory()

        response = self.client.post(reverse("api:withdraw", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZED)

    @authenticate
    def test_abandon_declaration_ok(self):
        company = CompanyFactory()
        user = authenticate.user

        # On doit pouvoir effectuer l'abandon en tant que pro seulement
        DeclarantRoleFactory(user=user, company=company)

        # On doit pouvoir effectuer l'abandon depuis les statuts générés par ces factories:
        declaration_factories = [
            OngoingInstructionDeclarationFactory,
            AwaitingInstructionDeclarationFactory,
            ObservationDeclarationFactory,
            AwaitingVisaDeclarationFactory,
            OngoingVisaDeclarationFactory,
            ObjectionDeclarationFactory,
        ]

        for declaration_factory in declaration_factories:
            declaration = declaration_factory(company=company)
            response = self.client.post(reverse("api:abandon", kwargs={"pk": declaration.id}), format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            declaration.refresh_from_db()
            latest_snapshot = declaration.snapshots.latest("creation_date")
            self.assertEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)
            self.assertEqual(latest_snapshot.action, Snapshot.SnapshotActions.ABANDON)
            self.assertEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)

    @authenticate
    def test_abandon_declaration_wrong_status(self):
        """
        On ne doit pas pouvoir abandoner une déclaration dans certains statuts
        """
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)

        # On ne doit pas pouvoir effectuer l'abandon depuis les statuts générés par ces factories:
        declaration_factories = [
            InstructionReadyDeclarationFactory,
            AuthorizedDeclarationFactory,
            RejectedDeclarationFactory,
            WithdrawnDeclarationFactory,
        ]

        for declaration_factory in declaration_factories:
            declaration = declaration_factory(company=company)
            response = self.client.post(reverse("api:abandon", kwargs={"pk": declaration.id}), format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            declaration.refresh_from_db()
            self.assertNotEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)

    @authenticate
    def test_abandon_declaration_other_company(self):
        """
        On ne doit pas pouvoir abandoner une déclaration d'une autre compagnie lors qu'on
        est déclarant·e
        """
        company = CompanyFactory()
        DeclarantRoleFactory(user=authenticate.user, company=company)

        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:abandon", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)

    @authenticate
    def test_abandon_declaration_instructor(self):
        """
        On ne doit pas pouvoir abandoner une déclaration en étant instructrice
        """
        InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:abandon", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)

    @authenticate
    def test_abandon_declaration_visor(self):
        """
        On ne doit pas pouvoir abandoner une déclaration en étant viseuse
        """
        VisaRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:abandon", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)

    def test_abandon_declaration_unauthenticated(self):
        """
        On ne doit pas pouvoir abandoner une déclaration sans être identifié·e
        """

        declaration = OngoingInstructionDeclarationFactory()

        response = self.client.post(reverse("api:abandon", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        declaration.refresh_from_db()
        self.assertNotEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)
