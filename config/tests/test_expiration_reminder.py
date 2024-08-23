from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from config.tasks import send_expiration_reminder
from data.factories import ObservationDeclarationFactory, SnapshotFactory
from data.models import Declaration


class TestExpirationReminder(TestCase):
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @mock.patch("config.email.send_sib_template")
    def test_send_reminders_before_expiration(self, mocked_brevo):
        """
        Un rappel doit être envoyé à l'auteur·ice d'une déclaration avant son expiration
        """
        template_number = 10
        today = timezone.now()
        declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=10,
        )
        # Le snapshot a été créé il y a 5 jours. Vu que la date d'expiration
        # est de 10 jours, on devrait envoyer l'email
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()

        send_expiration_reminder()

        mocked_brevo.assert_called_once_with(
            template_number,
            {**declaration.brevo_parameters, **{"REMAINING_DAYS": 5}},
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @mock.patch("config.email.send_sib_template")
    def test_multiple_snapshots(self, mocked_brevo):
        """
        Seulement le dernier snapshot « observation » ou « objection » sera pris en compte
        """
        template_number = 10
        today = timezone.now()
        declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=10,
        )

        snapshot_old = SnapshotFactory(
            declaration=declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=15,
        )
        # Le dernier snapshot a été créé il y a 5 jours. Vu que la date d'expiration
        # est de 10 jours, on devrait envoyer l'email
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot_old.creation_date = today - timedelta(days=25, minutes=1)
        snapshot.save()
        snapshot_old.save()

        send_expiration_reminder()

        mocked_brevo.assert_called_once_with(
            template_number,
            {**declaration.brevo_parameters, **{"REMAINING_DAYS": 5}},
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @mock.patch("config.email.send_sib_template")
    def test_do_not_send_early_reminders(self, mocked_brevo):
        """
        Un rappel ne doit pas être envoyé trop tôt
        """
        today = timezone.now()
        declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=10,
        )
        # Le snapshot a été créé il y a 4 jours. Vu que la date d'expiration
        # est de 10 jours, on a encore 6 jours devant nous. Donc pas d'envoi
        snapshot.creation_date = today - timedelta(days=4, minutes=1)
        snapshot.save()

        send_expiration_reminder()
        mocked_brevo.assert_not_called()

    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @mock.patch("config.email.send_sib_template")
    def test_do_not_send_late_reminders(self, mocked_brevo):
        """
        Un rappel ne doit pas être envoyé trop tard
        """
        today = timezone.now()
        declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=10,
        )
        # Le snapshot a été créé il y a 6 jours. Vu que la date d'expiration
        # est de 10 jours, on n'a que 4 jours devant nous. Donc pas d'envoi
        snapshot.creation_date = today - timedelta(days=6, minutes=1)
        snapshot.save()

        send_expiration_reminder()
        mocked_brevo.assert_not_called()
