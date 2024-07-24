from unittest import mock

from django.test import TestCase
from django.test.utils import override_settings


class TestExpirationReminder(TestCase):
    @mock.patch("config.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_EXPIRATION_REMINDER=1)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_send_reminders_before_expiration(self, _):
        """
        Un rappel doit être envoyé à l'auteur·ice d'une déclaration avant son expiration
        """
        pass
