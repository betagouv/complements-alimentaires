from django.test import TestCase
from data.utils.external_utils import InseeToken
from data.utils.date_utils import diff_dates
from django.utils import timezone
from datetime import timedelta as td
from unittest import mock


class InseeTokenTestCase(TestCase):
    # on n'utile volontairement pas de setUp class pour contrôler le nombre d'objet en base à un instant T.

    def test_load(self):
        # aucune instance en bdd
        self.assertFalse(InseeToken.objects.exists())

        # 1ère instance créée
        with mock.patch.object(InseeToken, "try_fetch_insee_token", return_value="some_valid_key"):
            token_1 = InseeToken.load()
        self.assertEqual(token_1.pk, 1)
        self.assertEqual(InseeToken.objects.count(), 1)

        token_1_expected_expiration = timezone.now() + td(seconds=604800 - 3600)
        token_1_expiration = token_1.expiration  # sauvegardé pour comparaison après
        self.assertTrue(diff_dates(token_1_expected_expiration, token_1_expiration) < 2)

        # la même instance est utilisée
        with mock.patch.object(InseeToken, "try_fetch_insee_token", return_value="some_valid_key"):
            token_2 = InseeToken.load()
        self.assertEqual(token_1.pk, token_2.pk)
        self.assertEqual(InseeToken.objects.count(), 1)

        # montre que l'expiration n'a pas changé
        self.assertEqual(token_1_expiration, token_2.expiration)

    def test_is_usable(self):
        """montre qu'un token est valide si la clé est bien renvoyée"""
        with mock.patch.object(InseeToken, "try_fetch_insee_token", return_value="some_valid_key"):
            token = InseeToken.load()
            self.assertEqual(token.key, "some_valid_key")
            self.assertTrue(token.usable)

    def test_is_not_usable_if_expired(self):
        """montre qu'un token est inutilisable s'il est expiré"""
        with mock.patch.object(InseeToken, "try_fetch_insee_token", return_value="some_valid_key"):
            token = InseeToken.load()
            token.expiration = timezone.now()
            token.save()
            self.assertFalse(token.usable)

    def test_is_not_usable_if_no_key(self):
        """montre qu'un token est inutilisable si une clé n'est pas renvoyée"""
        with mock.patch.object(InseeToken, "try_fetch_insee_token", return_value=None):
            token = InseeToken.load()
            self.assertFalse(token.usable)
