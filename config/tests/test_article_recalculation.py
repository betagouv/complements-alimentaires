from unittest.mock import patch

from django.test import TestCase

from config.tasks import recalculate_article_for_ongoing_declarations
from data.factories import (
    AuthorizedDeclarationFactory,
    OngoingInstructionDeclarationFactory,
)
from data.models import Declaration


def set_article_15(self):
    self.calculated_article = Declaration.Article.ARTICLE_15


def set_article_16(self):
    self.calculated_article = Declaration.Article.ARTICLE_16


class TestArticleRecalculation(TestCase):
    @patch.object(Declaration, "assign_calculated_article", set_article_15)
    def setUp(self):
        self.authorized_declaration = AuthorizedDeclarationFactory.create(name="authorized")
        self.authorized_declaration.assign_calculated_article()
        self.authorized_declaration.save()

        self.ongoing_instruction_declaration = OngoingInstructionDeclarationFactory.create(name="awaiting instruction")
        self.ongoing_instruction_declaration.assign_calculated_article()
        self.ongoing_instruction_declaration.save()

    def test_setup(self):
        self.assertEqual(self.authorized_declaration.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertEqual(self.ongoing_instruction_declaration.calculated_article, Declaration.Article.ARTICLE_15)

    @patch.object(Declaration, "assign_calculated_article", set_article_16)
    def test_recalculate_for_ongoing_declarations(self):
        """
        Les déclarations en cours sont modifiées mais non pas celles qui sont finalisées
        """
        recalculate_article_for_ongoing_declarations(Declaration.objects.all(), "change reason")

        self.authorized_declaration.refresh_from_db()
        self.assertEqual(
            self.authorized_declaration.calculated_article,
            Declaration.Article.ARTICLE_15,
            "La déclaration autorisée n'est pas modifiée",
        )
        self.ongoing_instruction_declaration.refresh_from_db()
        self.assertEqual(
            self.ongoing_instruction_declaration.calculated_article,
            Declaration.Article.ARTICLE_16,
            "La déclaration en cours est MAJ",
        )

    @patch.object(Declaration, "assign_calculated_article", set_article_16)
    def test_only_save_recalculated_articles(self):
        """
        Avoir une ligne dans l'historique que pour les déclarations où l'article a changé
        """
        self.assertEqual(self.authorized_declaration.history.count(), 3)
        self.assertEqual(self.ongoing_instruction_declaration.history.count(), 3)

        recalculate_article_for_ongoing_declarations(Declaration.objects.all(), "change reason")

        self.assertEqual(
            self.authorized_declaration.history.count(),
            3,
            "Sans modif, la déclaration autorisée n'a pas de lignes en plus dans l'historique",
        )
        self.assertEqual(
            self.ongoing_instruction_declaration.history.count(),
            4,
            "Avec modif, la déclaration en cours a une ligne en plus dans l'historique",
        )

    @patch.object(Declaration, "assign_calculated_article", set_article_16)
    def test_history_change_reason(self):
        """
        Quand un article est recalculé, c'est possible de sauvegarder un message comme raison de changement.
        Si le message est trop long les premiers 100 caractères seront sauvegardés.
        """
        long_reason = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ornare lacus id quam sodales, eget tellus."
        truncated_reason = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ornare lacus id quam sodales, eg"
        )
        self.assertNotEqual(self.ongoing_instruction_declaration.history.first().history_change_reason, long_reason)

        recalculate_article_for_ongoing_declarations(Declaration.objects.all(), long_reason)

        self.assertEqual(self.ongoing_instruction_declaration.history.first().history_change_reason, truncated_reason)
