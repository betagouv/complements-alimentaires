from django.test import TestCase
from django.test.utils import override_settings
from unittest.mock import patch, MagicMock

from config.tasks import import_control_emails
from data.models import ControlRoleEmail


class TestControlEmailImport(TestCase):
    @override_settings(GRIST_API_KEY="something")
    @override_settings(GRIST_SD_CONTROL_DOC_ID="something")
    @override_settings(GRIST_SD_CONTROL_TABLE_ID="something")
    @override_settings(GRIST_ANSES_CONTROL_DOC_ID="something")
    @override_settings(GRIST_ANSES_CONTROL_TABLE_ID="something")
    @patch("config.grist_api.requests")
    def test_import_control_emails_task(self, mock_requests):
        """
        Test que la tâche met à jour correctement les objets ControlRoleEmail
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [
                {"fields": {"mail": "new@Example.gouv.fr"}},
                {"fields": {"mail": "keep@Example.gouv.fr"}},  # test normalisation
                {"fields": {"mail": "new@example.gouv.fr"}},  # duplicate devrait être ignoré
                {"fields": {"mail": "new@example.org"}},  # adresse non-gouv devrait être ignoré
                {"fields": {"mail": ""}},  # adresse vide devrait être ignoré
            ]
        }
        mock_requests.get.return_value = mock_response

        # déjà en base, un mail à garder et un à supprimer
        ControlRoleEmail.objects.create(email="keep@example.gouv.fr")
        ControlRoleEmail.objects.create(email="delete@example.org")

        import_control_emails()

        self.assertEqual(ControlRoleEmail.objects.count(), 2)
        self.assertTrue(ControlRoleEmail.objects.filter(email="keep@example.gouv.fr").exists())
        self.assertTrue(ControlRoleEmail.objects.filter(email="new@example.gouv.fr").exists())
        self.assertFalse(ControlRoleEmail.objects.filter(email="delete@example.org").exists())
        self.assertFalse(ControlRoleEmail.objects.filter(email="new@example.org").exists())
        self.assertFalse(ControlRoleEmail.objects.filter(email="").exists())
