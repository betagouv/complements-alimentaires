from django.test import TestCase
from data.factories import UserFactory

from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):

    def test_empty_user_ko(self):
        with self.assertRaises(AssertionError):
            User.generate_username(first_name="", last_name="Ronaldo")

    def test_unicode_user(self):
        username = User.generate_username(first_name="🇨🇳 Kang-In 🇨🇳", last_name="DẤU HUYỀN")
        self.assertEqual(username, "kang-in.dau-huyen")

    def test_user_with_same_username(self):
        UserFactory(username="jean.dupon")
        username = User.generate_username(first_name="Jean", last_name="Dupon")
        self.assertEqual(username, "jean.dupon2")

        UserFactory(username="jean.dupon2")
        username = User.generate_username(first_name="jean", last_name="DUPON")
        self.assertEqual(username, "jean.dupon3")
