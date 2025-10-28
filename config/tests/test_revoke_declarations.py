from django.test import TestCase

from config import tasks
from data.factories import AuthorizedDeclarationFactory, OngoingInstructionDeclarationFactory
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

    def test_cannot_revoke_unauthorized_declarations(self):
        """
        Les déclarations qui ne sont pas autorisées ne peuvent pas basculer au statut
        retiré par l'administration
        """
        declaration = OngoingInstructionDeclarationFactory()

        tasks.revoke_authorisation_from_declarations(Declaration.objects.all())

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)
