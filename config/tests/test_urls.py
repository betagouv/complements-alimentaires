from importlib import reload

from django.test import TestCase, override_settings
from django.urls import clear_url_caches, reverse

import config.urls


class TestAdminUrlOverride(TestCase):
    def reload_urlconf(self):
        """Mise à jour des URLs suite à un changement dans les settings"""
        clear_url_caches()
        reload(config.urls)

    @override_settings(ADMIN_URL="test-admin")
    def test_admin_url_from_env(self):
        """
        L'URL de l'admin doit être pris de la variable d'environnement
        """
        self.reload_urlconf()
        self.assertEqual(reverse("admin:index"), "/test-admin/")
