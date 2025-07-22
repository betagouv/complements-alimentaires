from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from config import tasks
from data.factories import (
    AwaitingInstructionDeclarationFactory,
    ObjectionDeclarationFactory,
    ObservationDeclarationFactory,
    SnapshotFactory,
)
from data.models import Declaration


class TestExpiration(TestCase):
    def test_expire_observed_declaration(self):
        """
        Une déclaration en observation devrait être expirée si elle dépasse
        le temps alloué pour la réponse.
        """
        today = timezone.now()
        observed_declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=observed_declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()
        tasks.expire_declarations()

        observed_declaration.refresh_from_db()
        self.assertEqual(observed_declaration.status, Declaration.DeclarationStatus.ABANDONED)

    def test_expire_objected_declaration(self):
        """
        Une déclaration en objection devrait être expirée si elle dépasse
        le temps alloué pour la réponse.
        """
        today = timezone.now()
        objected_declaration = ObjectionDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=objected_declaration,
            status=Declaration.DeclarationStatus.OBJECTION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()
        tasks.expire_declarations()

        objected_declaration.refresh_from_db()
        self.assertEqual(objected_declaration.status, Declaration.DeclarationStatus.ABANDONED)

    def test_do_not_expire_before_cutoff(self):
        """
        Une déclaration ne doit pas être expirée avant le temps indiqué dans
        le dernier snapshot dans "expiration_days"
        """
        today = timezone.now()
        observed_declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=observed_declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=10,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5)
        snapshot.save()
        tasks.expire_declarations()

        observed_declaration.refresh_from_db()
        self.assertEqual(observed_declaration.status, Declaration.DeclarationStatus.OBSERVATION)

    def test_do_not_expire_other_declarations(self):
        """
        Les déclarations n'étant pas en observation ou objection ne doivent
        pas être expirées
        """
        today = timezone.now()
        instruction_declaration = AwaitingInstructionDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=instruction_declaration,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()
        tasks.expire_declarations()

        instruction_declaration.refresh_from_db()
        self.assertEqual(instruction_declaration.status, Declaration.DeclarationStatus.AWAITING_INSTRUCTION)

    def test_expire_all_ready_declarations(self):
        """
        Parmi plusieurs declarations, expirent toutes qui sont possibles,
        même quand il y a des erreurs avec autres
        """
        today = timezone.now()
        # declaration sans snapshot
        ObservationDeclarationFactory()

        instruction_declaration = AwaitingInstructionDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=instruction_declaration,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()

        observed_declaration_with_time = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=observed_declaration_with_time,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a un jour
        snapshot.creation_date = today - timedelta(days=1, minutes=1)
        snapshot.save()

        observed_declaration = ObservationDeclarationFactory()
        snapshot = SnapshotFactory(
            declaration=observed_declaration,
            status=Declaration.DeclarationStatus.OBSERVATION,
            expiration_days=5,
        )
        # On se dit que le snapshot a été créé il y a cinq jours
        snapshot.creation_date = today - timedelta(days=5, minutes=1)
        snapshot.save()

        tasks.expire_declarations()

        observed_declaration.refresh_from_db()
        self.assertEqual(observed_declaration.status, Declaration.DeclarationStatus.ABANDONED)
        observed_declaration_with_time.refresh_from_db()
        self.assertEqual(observed_declaration_with_time.status, Declaration.DeclarationStatus.OBSERVATION)
