from django.test import TestCase, override_settings

# from data.factories import AwaitingInstructionDeclarationFactory, InstructionReadyDeclarationFactory
# from data.models import Declaration


@override_settings(ENABLE_AUTO_VALIDATION=True)
class TestAutomaticApproval(TestCase):
    def test_draft_declaration_not_approved(self):
        """
        Une déclaration en brouillon ne devrait pas se valider toute seule
        """
        # declaration = InstructionReadyDeclarationFactory(status=Declaration.DeclarationStatus.DRAFT)
        pass

    def test_awaiting_declaration_approved_art_15(self):
        """
        Une déclaration en attente d'instruction doit se valider si aucune action
        d'instruction n'a été effectuée dessus
        """
        # declaration = AwaitingInstructionDeclarationFactory()
        pass

    def test_email_sent_declaration_approved(self):
        """
        L'email d'approbation doit être envoyé lors d'une approbation automatique
        """
        # declaration = AwaitingInstructionDeclarationFactory()
        pass

    @override_settings(ENABLE_AUTO_VALIDATION=False)
    def test_awaiting_declaration_not_approved_without_setting(self):
        """
        Le bot ne doit pas approuver des déclarations si le setting ENABLE_AUTO_VALIDATION
        n'est pas True
        """
        # declaration = AwaitingInstructionDeclarationFactory()
        pass

    def test_awaiting_declaration_not_approved_art_15_vig(self):
        """
        Une déclaration en attente d'instruction doit se valider si aucune action
        d'instruction n'a été effectuée dessus
        """
        # declaration = AwaitingInstructionDeclarationFactory()
        pass

    def test_awaiting_declaration_not_approved_art_16(self):
        """
        Une déclaration en attente d'instruction doit se valider si aucune action
        d'instruction n'a été effectuée dessus
        """
        # declaration = AwaitingInstructionDeclarationFactory()
        pass

    def test_awaiting_declaration_not_approved_art_anses(self):
        """
        Une déclaration en attente d'instruction doit se valider si aucune action
        d'instruction n'a été effectuée dessus
        """
        # declaration = AwaitingInstructionDeclarationFactory()
        pass

    def test_awaiting_declaration_not_approved_instructed(self):
        """
        Une déclaration en attente d'instruction ne doit pas se valider si des
        actions d'instruction ont été effectuées dessus, par exemple des observations,
        objections, requêtes de visa, etc.
        """
        pass

    def test_ongoing_declaration_not_approved(self):
        """
        Une déclaration dont l'instruction est en cours ne doit pas se valider
        toute seule
        """
        pass

    def test_objected_declaration_not_approved(self):
        """
        Une déclaration en objection ne doit pas se valider toute seule
        """
        pass

    def test_observed_declaration_not_approved(self):
        """
        Une déclaration en observation ne doit pas se valider toute seule
        """
        pass

    def test_abandoned_declaration_not_approved(self):
        """
        Une déclaration en abandon ne doit pas se valider toute seule
        """
        pass

    def test_refused_declaration_not_approved(self):
        """
        Une déclaration refusée ne doit pas se valider toute seule
        """
        pass

    def test_withdrawn_declaration_not_approved(self):
        """
        Une déclaration retirée du marché ne doit pas se valider toute seule
        """
        pass
