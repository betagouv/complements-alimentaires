from django.test import TestCase

from config import tasks
from data.factories import AuthorizedDeclarationFactory
from data.models import Declaration


class TestWithdraw(TestCase):
    def test_withdraw_declarations(self):
        """
        Déclarations autorisées peuvent être retirées du marché par l'administration
        """
        declaration = AuthorizedDeclarationFactory()

        tasks.withdraw_declarations(Declaration.objects.all())

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.WITHDRAWN_BY_ADMINISTRATION)
