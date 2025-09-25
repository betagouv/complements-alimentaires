from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from data.models import ControlRole, ControlRoleEmail

User = get_user_model()


class TestAssignControlRolesCommand(TestCase):
    def setUp(self):
        self.user1 = TestAssignControlRolesCommand._create_user("user1@example.com")
        self.user2 = TestAssignControlRolesCommand._create_user("user2@example.com")
        self.user3 = TestAssignControlRolesCommand._create_user("user3@example.com")
        self.inactive_user = TestAssignControlRolesCommand._create_user("inactive@example.com", False)

    @staticmethod
    def _create_user(email, active=True):
        return User.objects.create_user(email=email, username=email, password="1234", is_active=active)

    def test_assign_roles_based_on_email_list(self):
        """Le rôle contrôle est assigné depuis les modèles ControlRoleEmail"""

        ControlRoleEmail.objects.create(email="user1@example.com")
        ControlRoleEmail.objects.create(email="user2@example.com")

        out = StringIO()
        call_command("assign_control_roles", stdout=out)

        self.assertTrue(ControlRole.objects.filter(user=self.user1).exists())
        self.assertTrue(ControlRole.objects.filter(user=self.user2).exists())
        self.assertFalse(ControlRole.objects.filter(user=self.user3).exists())

        self.assertIn("✓ Added control role to user1@example.com", out.getvalue())
        self.assertIn("✓ Added control role to user2@example.com", out.getvalue())

    def test_remove_roles_not_in_email_list(self):
        """Les rôles contrôle obsolètes sont supprimés"""

        ControlRole.objects.create(user=self.user1)
        ControlRole.objects.create(user=self.user2)

        ControlRoleEmail.objects.create(email="user1@example.com")

        call_command("assign_control_roles")

        # user1 reste, user2 ne devrait plus avoir le rôle
        self.assertTrue(ControlRole.objects.filter(user=self.user1).exists())
        self.assertFalse(ControlRole.objects.filter(user=self.user2).exists())
        self.assertFalse(ControlRole.objects.filter(user=self.user2).exists())

    def test_always_persist_roles_are_preserved(self):
        """Les rôles de contrôle avec le paramètre `always_persist` doivent rester"""
        ControlRole.objects.create(user=self.user1, always_persist=True)
        ControlRole.objects.create(user=self.user2, always_persist=False)

        # La liste des emails est vide. user1 doit rester néanomins car `always_persist = True`
        call_command("assign_control_roles")

        self.assertTrue(ControlRole.objects.filter(user=self.user1).exists())
        self.assertFalse(ControlRole.objects.filter(user=self.user2).exists())

    def test_dry_run_mode(self):
        """Le dry run ne fait pas de modifs en base"""
        ControlRoleEmail.objects.create(email="user1@example.com")

        out = StringIO()
        call_command("assign_control_roles", "--dry-run", stdout=out)

        self.assertFalse(ControlRole.objects.exists())
        self.assertIn("DRY RUN - No changes made", out.getvalue())
        self.assertIn("Emails to add: 1", out.getvalue())

    def test_inactive_users_are_ignored(self):
        """Les utilisateur·ices non-actif·ves ne doivent pas être pris en compte"""
        ControlRoleEmail.objects.create(email="inactive@example.com")
        call_command("assign_control_roles")

        self.assertFalse(ControlRole.objects.filter(user=self.inactive_user).exists())

    def test_case_insensitive_email_matching(self):
        """L'assignation se fait en ignorant les majuscules/minuscules"""
        ControlRoleEmail.objects.create(email="USER1@EXAMPLE.COM")
        call_command("assign_control_roles")

        self.assertTrue(ControlRole.objects.filter(user=self.user1).exists())

    def test_control_role_assigned_on_user_creation(self):
        """Un nouveau compte doit avoir le rôle contrôle si l'email est dans la liste"""

        ControlRoleEmail.objects.create(email="newuser@example.com")

        user = TestAssignControlRolesCommand._create_user("newuser@example.com")

        self.assertTrue(ControlRole.objects.filter(user=user).exists())

    def test_control_role_not_assigned_when_email_not_in_list(self):
        """Un nouveau compte ne doit pas avoir le rôle contrôle si l'email n'est pas dans la liste"""
        user = TestAssignControlRolesCommand._create_user("not_in_list@example.com")

        self.assertFalse(ControlRole.objects.filter(user=user).exists())
