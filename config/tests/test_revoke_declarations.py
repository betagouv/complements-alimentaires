from django.test import TestCase

from config import tasks
from data.factories import AuthorizedDeclarationFactory
from data.models import Declaration


class TestRevokeDeclarations(TestCase):
    def test_revoke_authorisation_from_declarations(self):
        """
        Déclarations autorisées peuvent être retirées du marché par l'administration
        """
        declaration = AuthorizedDeclarationFactory()

        tasks.revoke_authorisation_from_declarations(Declaration.objects.all())

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZATION_REVOKED)
