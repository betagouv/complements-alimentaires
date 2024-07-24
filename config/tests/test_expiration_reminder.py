from django.test import TestCase


class TestExpirationReminder(TestCase):
    def test_send_reminders_before_expiration(self, _):
        """
        Un rappel doit être envoyé à l'auteur·ice d'une déclaration avant son expiration
        """
        pass
