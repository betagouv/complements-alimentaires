from django.test import TestCase

from config.tasks import update_market_ready_counts
from data.factories import (
    AuthorizedDeclarationFactory,
    AwaitingInstructionDeclarationFactory,
    CompanyFactory,
    RejectedDeclarationFactory,
)
from data.models import Declaration


class TestUpdateMarketReadyCountsTask(TestCase):
    def test_update_market_ready_counts_task(self):
        """
        Test que la tâche met à jour correctement le cache des counts market-ready
        """
        company1 = CompanyFactory()
        company2 = CompanyFactory()
        company3 = CompanyFactory()

        # Company1: 2 déclarations market-ready
        AwaitingInstructionDeclarationFactory(company=company1, overridden_article=Declaration.Article.ARTICLE_15)
        AwaitingInstructionDeclarationFactory(
            company=company1, overridden_article=Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
        )

        # Company2: 1 déclaration market-ready, 1 non market-ready
        AuthorizedDeclarationFactory(company=company2)
        AwaitingInstructionDeclarationFactory(
            company=company2,
            overridden_article=Declaration.Article.ARTICLE_16,  # Non market-ready
        )

        # Company3: 0 déclarations market-ready
        RejectedDeclarationFactory(company=company3)  # Non market-ready

        update_market_ready_counts()
        company1.refresh_from_db()
        company2.refresh_from_db()
        company3.refresh_from_db()

        self.assertEqual(company1.market_ready_count_cache, 2)
        self.assertEqual(company2.market_ready_count_cache, 1)
        self.assertEqual(company3.market_ready_count_cache, 0)

        # Vérifier que le timestamp est mis à jour
        self.assertIsNotNone(company1.market_ready_count_updated_at)
        self.assertIsNotNone(company2.market_ready_count_updated_at)
        self.assertIsNotNone(company3.market_ready_count_updated_at)

    def test_company_without_declarations(self):
        """
        Test une entreprise sans déclarations
        """
        company = CompanyFactory()

        update_market_ready_counts()
        company.refresh_from_db()

        self.assertEqual(company.market_ready_count_cache, 0)
        self.assertIsNotNone(company.market_ready_count_updated_at)
