from django.test import TestCase
from unittest import mock

from config import tasks
from data.factories import (
    AuthorizedDeclarationFactory,
    OngoingInstructionDeclarationFactory,
    IngredientFactory,
    DeclaredIngredientFactory,
)
from data.models import Declaration, IngredientStatus


class TestRevokeDeclarations(TestCase):
    @mock.patch("config.email.send_sib_template")
    def test_revoke_authorisation_from_declarations(self, mocked_brevo):
        """
        Déclarations autorisées peuvent être retirées du marché par l'administration
        """
        ingredient = IngredientFactory(status=IngredientStatus.AUTHORIZATION_REVOKED)
        declaration = AuthorizedDeclarationFactory()
        DeclaredIngredientFactory(declaration=declaration, ingredient=ingredient)

        tasks.revoke_authorisation_from_declarations(Declaration.objects.all(), ingredient)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AUTHORIZATION_REVOKED)
        self.assertIsNotNone(declaration.revoked_ingredient)
        self.assertEqual(declaration.revoked_ingredient["id"], ingredient.id)
        self.assertEqual(declaration.revoked_ingredient["name"], ingredient.name)
        self.assertEqual(declaration.revoked_ingredient["model"], "Ingredient")
        template_number = 37
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
        ingredient = IngredientFactory(status=IngredientStatus.AUTHORIZATION_REVOKED)
        declaration = OngoingInstructionDeclarationFactory()
        DeclaredIngredientFactory(declaration=declaration, ingredient=ingredient)

        tasks.revoke_authorisation_from_declarations(Declaration.objects.all(), ingredient)

        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)
        self.assertIsNone(declaration.revoked_ingredient)
        mocked_brevo.assert_not_called()

    # TODO: test cannot revoke declarations if ingredient isn't revoked
    # TODO: test cannot revoke declaration if ingredient isn't in declared ingredients?
    # TODO: test a declaration authorized with a revoked
