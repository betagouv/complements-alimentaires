from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ..factories import SupervisionClaimFactory, UserFactory


class BaseSolicitationTestCase(TestCase):
    def setUp(self):
        self.solicitation = SupervisionClaimFactory()

    def test_action_is_processed(self):
        self.assertFalse(self.solicitation.processed_at)
        user = UserFactory()
        self.solicitation.accept(processor=user)
        self.assertTrue(self.solicitation.processed_at)

    def test_soliciation_cant_be_created_with_process_fields(self):
        # Erreur à la création
        with self.assertRaises(ValidationError):
            SupervisionClaimFactory(processed_at=timezone.now(), processor=UserFactory(), processed_action="accept")

        # Pas d'erreur à la modification
        try:
            self.solicitation.processed_at = timezone.now()
            self.solicitation.processor = UserFactory()
            self.solicitation.processed_action = "accept"
        except ValidationError:
            self.fail("ValidationError should not be raised")

    def test_soliciation_process_requires_all_process_field(self):
        self.solicitation.processed_at = timezone.now()
        with self.assertRaises(ValidationError):
            self.solicitation.save()
