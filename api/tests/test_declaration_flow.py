from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    AwaitingInstructionDeclarationFactory,
    AwaitingVisaDeclarationFactory,
    CompanyFactory,
    DeclarantRoleFactory,
    InstructionReadyDeclarationFactory,
    InstructionRoleFactory,
    ObservationDeclarationFactory,
    OngoingInstructionDeclarationFactory,
    VisaRoleFactory,
)
from data.models import Declaration

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
        self.assertEqual("Le complément doit comporter au moins un ingrédient", json_errors["nonFieldErrors"][0])

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

        response = self.client.post(reverse("api:observe_no_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBSERVATION)

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

        response = self.client.post(reverse("api:observe_with_visa", kwargs={"pk": declaration.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        declaration.refresh_from_db()
        self.assertEqual(declaration.post_validation_status, Declaration.DeclarationStatus.OBSERVATION)
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_VISA)

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
