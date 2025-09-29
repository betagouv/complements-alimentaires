from django.test import TestCase
from django.test.utils import override_settings
from unittest.mock import patch, MagicMock

from config.tasks import import_control_emails
from data.models import ControlRoleEmail


class TestControlEmailImport(TestCase):
    @override_settings(GRIST_API_KEY="something")
    @patch("config.grist_api.requests")
    def test_import_control_emails_task(self, mock_requests):
        """
        Test que la tâche met à jour correctement les objets ControlRoleEmail
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [
                {"fields": {"mail": "new@example.org"}},
                {"fields": {"mail": "keep@example.org"}},
                {"fields": {"mail": "keep@example.org"}},  # duplicate devrait être ignoré
                {"fields": {"mail": ""}},  # adresse vide devrait être ignoré
            ]
        }
        mock_requests.get.return_value = mock_response

        # déjà en base, un mail à garder et un à supprimer
        ControlRoleEmail.objects.create(email="keep@example.org")
        ControlRoleEmail.objects.create(email="delete@example.org")

        import_control_emails()

        self.assertEqual(ControlRoleEmail.objects.count(), 2)
        self.assertTrue(ControlRoleEmail.objects.filter(email="keep@example.org").exists())
        self.assertTrue(ControlRoleEmail.objects.filter(email="new@example.org").exists())
        self.assertFalse(ControlRoleEmail.objects.filter(email="delete@example.org").exists())
        self.assertFalse(ControlRoleEmail.objects.filter(email="").exists())
