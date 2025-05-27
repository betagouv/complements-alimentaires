from datetime import timedelta
from unittest import mock

from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase

from config import tasks
from data.factories import (
    AuthorizedDeclarationFactory,
    CompanyFactory,
    DeclarantRoleFactory,
    InstructionReadyDeclarationFactory,
    InstructionRoleFactory,
    ObjectionDeclarationFactory,
    ObservationDeclarationFactory,
    OngoingInstructionDeclarationFactory,
    OngoingVisaDeclarationFactory,
    SnapshotFactory,
    VisaRoleFactory,
)
from data.models import Declaration

from .utils import authenticate


@override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
@override_settings(CONTACT_EMAIL="contact@example.com")
@mock.patch("config.email.send_sib_template")
class TestDeclarationFlow(APITestCase):
    @authenticate
    def test_submit_declaration(self, mocked_brevo):
        """
        Passage du DRAFT -> AWAITING_INSTRUCTION = Template 3
        """
        declarant_role = DeclarantRoleFactory(user=authenticate.user)
        company = declarant_role.company
        template_number = 3
        declaration = InstructionReadyDeclarationFactory(author=authenticate.user, company=company)

        self.client.post(reverse("api:submit_declaration", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_observe_declaration(self, mocked_brevo):
        """
        Passage du ONGOING_INSTRUCTION -> OBSERVATION = Template 4
        """
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory(instructor=instructor)
        template_number = 4

        self.client.post(reverse("api:observe_no_visa", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_authorize_declaration(self, mocked_brevo):
        """
        Passage du ONGOING_INSTRUCTION -> AUTHORIZED = Template 6
        """
        instructor = InstructionRoleFactory(user=authenticate.user)
        declaration = OngoingInstructionDeclarationFactory(instructor=instructor)
        template_number = 6

        self.client.post(reverse("api:authorize_no_visa", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_resubmit_declaration(self, mocked_brevo):
        """
        Passage du OBSERVATION -> AWAITING_INSTRUCTION = Pas d'email
        """
        company = CompanyFactory()
        declarant = DeclarantRoleFactory(user=authenticate.user, company=company)
        declaration = ObservationDeclarationFactory(author=declarant.user, company=company)

        self.client.post(reverse("api:resubmit_declaration", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_not_called()

    @authenticate
    def test_authorize_with_visa(self, mocked_brevo):
        """
        Passage de ONGOING_VISA à AUTHORIZED = Template 6
        """
        VisaRoleFactory(user=authenticate.user)
        template_number = 6

        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.AUTHORIZED,
            post_validation_producer_message="À authoriser",
            post_validation_expiration_days=12,
        )

        self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_refuse_with_visa(self, mocked_brevo):
        """
        Passage de ONGOING_VISA à REJECTED = Template 7
        """
        VisaRoleFactory(user=authenticate.user)
        template_number = 7

        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.REJECTED,
            post_validation_producer_message="À refuser",
            post_validation_expiration_days=20,
        )

        self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_observe_with_visa(self, mocked_brevo):
        """
        Passage de ONGOING_VISA à OBSERVATION = Template 4
        """
        VisaRoleFactory(user=authenticate.user)
        template_number = 4

        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.OBSERVATION,
            post_validation_producer_message="Observation",
            post_validation_expiration_days=23,
        )

        self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_observe_with_visa_modifying_original(self, mocked_brevo):
        """
        Passage de ONGOING_VISA à OBSERVATION = Template 4
        """
        VisaRoleFactory(user=authenticate.user)
        template_number = 4

        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.REJECTED,
            post_validation_producer_message="À refuser",
            post_validation_expiration_days=20,
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
        self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), body, format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_object_with_visa(self, mocked_brevo):
        """
        Passage de ONGOING_VISA à OBJECTION = Template 5
        """
        VisaRoleFactory(user=authenticate.user)
        template_number = 5

        declaration = OngoingVisaDeclarationFactory(
            post_validation_status=Declaration.DeclarationStatus.OBJECTION,
            post_validation_producer_message="Objection",
            post_validation_expiration_days=22,
        )

        self.client.post(reverse("api:accept_visa", kwargs={"pk": declaration.id}), format="json")

        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @authenticate
    def test_withdraw(self, mocked_brevo):
        """
        Passage de AUTHORIZED à WITHDRAWN = Template 8
        """
        declaration = AuthorizedDeclarationFactory(author=authenticate.user)
        template_number = 8
        payload = {"effective_withdrawal_date": "2026-05-08"}

        self.client.post(reverse("api:withdraw", kwargs={"pk": declaration.id}), payload, format="json")
        declaration.refresh_from_db()
        brevo_parameters = declaration.brevo_parameters

        self.assertEqual(brevo_parameters["EFFECTIVE_WITHDRAWAL_DATE"], "vendredi 8 mai 2026")

        mocked_brevo.assert_called_once_with(
            template_number,
            brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    def test_expire_observed_declaration(self, mocked_brevo):
        """
        Passage de OBSERVATION à ABANDONED = Template 9
        """
        template_number = 9
        today = timezone.now()
        observed_declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=observed_declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()
        tasks.expire_declarations()

        mocked_brevo.assert_called_once_with(
            template_number,
            observed_declaration.brevo_parameters,
            observed_declaration.author.email,
            observed_declaration.author.get_full_name(),
        )

    def test_expire_objected_declaration(self, mocked_brevo):
        """
        Passage de OBJECTION à ABANDONED = Template 9
        """
        template_number = 9
        today = timezone.now()
        objected_declaration = ObjectionDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=objected_declaration,
            status=Declaration.DeclarationStatus.OBJECTION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()
        tasks.expire_declarations()

        mocked_brevo.assert_called_once_with(
            template_number,
            objected_declaration.brevo_parameters,
            objected_declaration.author.email,
            objected_declaration.author.get_full_name(),
        )
