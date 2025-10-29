from django.test import TestCase
from unittest import mock

from config import tasks
from data.factories import AuthorizedDeclarationFactory, OngoingInstructionDeclarationFactory, IngredientFactory
from data.models import Declaration


class TestRevokeDeclarations(TestCase):
    @mock.patch("config.email.send_sib_template")
    def test_revoke_authorisation_from_declarations(self, mocked_brevo):
        """
        Déclarations autorisées peuvent être retirées du marché par l'administration
        """
        ingredient = IngredientFactory(revoked_detail="Some detail")
        declaration = AuthorizedDeclarationFactory()

        tasks.revoke_authorisation_from_declarations(Declaration.objects.all(), ingredient)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZATION_REVOKED)
        template_number = 99  # TODO: use proper number
        mocked_brevo.assert_called_once_with(
            template_number,
            {
                "INGREDIENT_NAME": ingredient.name,
                "PRODUCT_NAME": declaration.name,
                "DECLARATION_LINK": declaration.producer_url,
                "INGREDIENT_LINK": ingredient.url,
            },
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @mock.patch("config.email.send_sib_template")
    def test_cannot_revoke_unauthorized_declarations(self, mocked_brevo):
        """
        Les déclarations qui ne sont pas autorisées ne peuvent pas basculer au statut
        retiré par l'administration
        """
        ingredient = IngredientFactory()
        declaration = OngoingInstructionDeclarationFactory()

        tasks.revoke_authorisation_from_declarations(Declaration.objects.all(), ingredient)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)
        mocked_brevo.assert_not_called()
