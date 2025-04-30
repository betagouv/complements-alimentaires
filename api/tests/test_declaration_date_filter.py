from datetime import datetime

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase

from data.factories import AuthorizedDeclarationFactory, InstructionRoleFactory, SnapshotFactory
from data.models import Declaration, Snapshot

from .utils import authenticate


class DeclarationFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.declaration = AuthorizedDeclarationFactory()

        # Snapshot pour la soumission
        cls.submission_snapshot = SnapshotFactory(
            declaration=cls.declaration,
            action=Snapshot.SnapshotActions.SUBMIT,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
        )
        cls.submission_snapshot.creation_date = timezone.make_aware(datetime(2024, 6, 15))
        cls.submission_snapshot.save()

        # Snapshot pour la décision
        cls.decision_snapshot = SnapshotFactory(
            declaration=cls.declaration,
            action=Snapshot.SnapshotActions.AUTHORIZE_NO_VISA,
            status=Declaration.DeclarationStatus.AUTHORIZED,
        )
        cls.decision_snapshot.creation_date = timezone.make_aware(datetime(2024, 7, 1))
        cls.decision_snapshot.save()

    @authenticate
    def test_submission_date_filters(self):
        InstructionRoleFactory(user=authenticate.user)
        url = reverse("api:list_all_declarations")

        response = self.client.get(f"{url}?submission_date_after=2024-06-10")
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.client.get(f"{url}?submission_date_before=2024-06-20")
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.client.get(f"{url}?submission_date_after=2024-07-01")
        self.assertEqual(len(response.json()["results"]), 0)

    @authenticate
    def test_decision_date_filters(self):
        InstructionRoleFactory(user=authenticate.user)
        url = reverse("api:list_all_declarations")

        response = self.client.get(f"{url}?decision_date_after=2024-06-15")
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.client.get(f"{url}?decision_date_before=2024-07-15")
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.client.get(f"{url}?decision_date_after=2024-08-01")
        self.assertEqual(len(response.json()["results"]), 0)

    @authenticate
    def test_invalid_date_format(self):
        InstructionRoleFactory(user=authenticate.user)
        url = reverse("api:list_all_declarations")
        response = self.client.get(f"{url}?submission_date_after=06-10-2024")  # Mauvais format
        self.assertEqual(len(response.json()["results"]), 0)

    @authenticate
    def test_timezone_handling(self):
        InstructionRoleFactory(user=authenticate.user)
        # Snapshot créé en UTC+2
        SnapshotFactory(creation_date=timezone.make_aware(datetime(2024, 6, 15, 2, 0)))  # 2AM UTC+2

        # Avec le filtre date ça devrait matcher même si c'est juin 14 UTC
        response = self.client.get(f"{reverse('api:list_all_declarations')}?submission_date_after=2024-06-15")
        self.assertEqual(len(response.json()["results"]), 1)
