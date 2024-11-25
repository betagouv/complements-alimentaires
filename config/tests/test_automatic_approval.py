from unittest import mock

from django.test import TestCase, override_settings
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from config.tasks import approve_declarations
from data.factories import (
    AwaitingInstructionDeclarationFactory,
    InstructionReadyDeclarationFactory,
    ObjectionDeclarationFactory,
    ObservationDeclarationFactory,
    OngoingInstructionDeclarationFactory,
    SnapshotFactory,
)
from data.models import Declaration, Snapshot


@override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
@override_settings(CONTACT_EMAIL="contact@example.com")
@mock.patch("config.email.send_sib_template")
@override_settings(ENABLE_AUTO_VALIDATION=True)
class TestAutomaticApproval(TestCase):
    @staticmethod
    def _create_submission_snapshot(declaration):
        submission_date = timezone.now() - relativedelta(months=3)
        snapshot = SnapshotFactory(
            action=Snapshot.SnapshotActions.SUBMIT,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            declaration=declaration,
        )
        snapshot.creation_date = submission_date
        snapshot.save()

    def test_draft_declaration_not_approved(self, mocked_brevo):
        """
        Une déclaration en brouillon ne devrait pas se valider toute seule
        """
        declaration = InstructionReadyDeclarationFactory(status=Declaration.DeclarationStatus.DRAFT)
        approve_declarations()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.DRAFT)
        mocked_brevo.assert_not_called()

    def test_awaiting_declaration_approved_art_15(self, _):
        """
        Une déclaration en attente d'instruction doit se valider si :
         * elle a l'article 15 ou 15 population à risque
         * aucune action d'instruction n'a été effectuée dessus
         * son snapshot de soumission date de plus de deux mois.
        """
        declaration_15 = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        TestAutomaticApproval._create_submission_snapshot(declaration_15)

        declaration_high_risk_population = AwaitingInstructionDeclarationFactory(
            overriden_article=Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
        )
        TestAutomaticApproval._create_submission_snapshot(declaration_high_risk_population)

        approve_declarations()
        declaration_15.refresh_from_db()
        declaration_high_risk_population.refresh_from_db()

        self.assertEqual(declaration_15.status, Declaration.DeclarationStatus.AUTHORIZED)
        latest_snapshot_15 = declaration_15.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot_15.action, Snapshot.SnapshotActions.AUTOMATICALLY_AUTHORIZE)

        self.assertEqual(declaration_high_risk_population.status, Declaration.DeclarationStatus.AUTHORIZED)
        latest_snapshot_hrp = declaration_high_risk_population.snapshots.latest("creation_date")
        self.assertEqual(latest_snapshot_hrp.action, Snapshot.SnapshotActions.AUTOMATICALLY_AUTHORIZE)

    def test_email_sent_declaration_approved(self, mocked_brevo):
        """
        L'email d'approbation doit être envoyé lors d'une approbation automatique
        """
        declaration = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()

        template_number = 6
        mocked_brevo.assert_called_once_with(
            template_number,
            declaration.brevo_parameters,
            declaration.author.email,
            declaration.author.get_full_name(),
        )

    @override_settings(ENABLE_AUTO_VALIDATION=False)
    def test_awaiting_declaration_not_approved_without_setting(self, mocked_brevo):
        """
        Le bot ne doit pas approuver des déclarations si le setting ENABLE_AUTO_VALIDATION
        n'est pas True
        """
        declaration = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        mocked_brevo.assert_not_called()

    def test_awaiting_declaration_not_approved_art_15_vig(self, mocked_brevo):
        """
        Une déclaration en attente d'instruction de doit pas se valider si elle a l'article
        15 vigilance
        """
        declaration = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15_WARNING)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        mocked_brevo.assert_not_called()

    def test_awaiting_declaration_not_approved_art_16(self, mocked_brevo):
        """
        Une déclaration en attente d'instruction de doit pas se valider si elle a l'article 16
        """
        declaration = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_16)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        mocked_brevo.assert_not_called()

    def test_awaiting_declaration_not_approved_art_anses(self, mocked_brevo):
        """
        Une déclaration en attente d'instruction de doit pas se valider si elle a l'article ANSES
        """
        declaration = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ANSES_REFERAL)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        mocked_brevo.assert_not_called()

    def test_awaiting_declaration_not_approved_no_article(self, mocked_brevo):
        """
        Une déclaration en attente d'instruction de doit pas se valider si elle n'a pas d'article
        """
        declaration = AwaitingInstructionDeclarationFactory()
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        mocked_brevo.assert_not_called()

    def test_awaiting_declaration_not_approved_instructed(self, mocked_brevo):
        """
        Une déclaration en attente d'instruction ne doit pas se valider si des
        actions d'instruction ont été effectuées dessus, par exemple des observations,
        objections, requêtes de visa, etc.
        """
        declaration = AwaitingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        # On crée un autre snapshot indiquant que la déclaration a subi des actions autres
        # que celle de la soumission
        observation_date = timezone.now() - relativedelta(months=4)
        snapshot = SnapshotFactory(
            action=Snapshot.SnapshotActions.OBSERVE_NO_VISA,
            status=Declaration.DeclarationStatus.OBSERVATION,
            declaration=declaration,
        )
        snapshot.creation_date = observation_date
        snapshot.save()

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)
        mocked_brevo.assert_not_called()

    def test_ongoing_declaration_not_approved(self, mocked_brevo):
        """
        Une déclaration dont l'instruction est en cours ne doit pas se valider
        toute seule
        """
        declaration = OngoingInstructionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ONGOING_INSTRUCTION)
        mocked_brevo.assert_not_called()

    def test_observed_declaration_not_approved(self, mocked_brevo):
        """
        Une déclaration en observation ne doit pas se valider toute seule
        """
        declaration = ObservationDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBSERVATION)
        mocked_brevo.assert_not_called()

    def test_objected_declaration_not_approved(self, mocked_brevo):
        """
        Une déclaration en objection ne doit pas se valider toute seule
        """
        declaration = ObjectionDeclarationFactory(overriden_article=Declaration.Article.ARTICLE_15)
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.OBJECTION)
        mocked_brevo.assert_not_called()

    def test_abandoned_declaration_not_approved(self, mocked_brevo):
        """
        Une déclaration en abandon ne doit pas se valider toute seule
        """
        declaration = InstructionReadyDeclarationFactory(
            status=Declaration.DeclarationStatus.ABANDONED, overriden_article=Declaration.Article.ARTICLE_15
        )
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.ABANDONED)
        mocked_brevo.assert_not_called()

    def test_refused_declaration_not_approved(self, mocked_brevo):
        """
        Une déclaration refusée ne doit pas se valider toute seule
        """
        declaration = InstructionReadyDeclarationFactory(
            status=Declaration.DeclarationStatus.REJECTED, overriden_article=Declaration.Article.ARTICLE_15
        )
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.REJECTED)
        mocked_brevo.assert_not_called()

    def test_withdrawn_declaration_not_approved(self, mocked_brevo):
        """
        Une déclaration retirée du marché ne doit pas se valider toute seule
        """
        declaration = InstructionReadyDeclarationFactory(
            status=Declaration.DeclarationStatus.WITHDRAWN, overriden_article=Declaration.Article.ARTICLE_15
        )
        TestAutomaticApproval._create_submission_snapshot(declaration)

        approve_declarations()
        declaration.refresh_from_db()
        self.assertEqual(declaration.status, Declaration.DeclarationStatus.WITHDRAWN)
        mocked_brevo.assert_not_called()
