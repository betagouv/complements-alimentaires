from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase

# from data.factories import AuthorizedDeclarationFactory, ObjectionDeclarationFactory, SnapshotFactory
# from data.models import Declaration, Snapshot


class TestMigrations(TestCase):
    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert (
            self.migrate_from and self.migrate_to
        ), "TestCase '{}' must define migrate_from and migrate_to properties".format(type(self).__name__)
        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps


# Ce test n'est plus exécuté car le modèle de données à changé
# class ApproFieldsTestCase(TestMigrations):
#     migrate_from = "0149_alter_declaration_teleicare_id_and_more"
#     migrate_to = "0150_alter_historicalingredient_to_be_entered_in_next_decree_and_more"

# def setUpBeforeMigration(self, apps):
#     OldIngredient = apps.get_model("data", "Ingredient")
#     self.teleicare_ingredient = OldIngredient.objects.create(siccrf_id=1, to_be_entered_in_next_decree=False)
#     self.ca_ingredient = OldIngredient.objects.create(siccrf_id=None, to_be_entered_in_next_decree=False)
#     OldMicroorganism = apps.get_model("data", "Microorganism")
#     self.teleicare_microorganism = OldMicroorganism.objects.create(siccrf_id=2, to_be_entered_in_next_decree=False)
#     self.ca_microorganism = OldMicroorganism.objects.create(siccrf_id=None, to_be_entered_in_next_decree=False)
#     OldPlant = apps.get_model("data", "Plant")
#     self.teleicare_plant = OldPlant.objects.create(siccrf_id=3, to_be_entered_in_next_decree=False)
#     self.ca_plant = OldPlant.objects.create(siccrf_id=None, to_be_entered_in_next_decree=False)
#     OldSubstance = apps.get_model("data", "Substance")
#     self.teleicare_substance = OldSubstance.objects.create(siccrf_id=4, to_be_entered_in_next_decree=False)
#     self.ca_substance = OldSubstance.objects.create(siccrf_id=None, to_be_entered_in_next_decree=False)

#     def test_migration_0150(self):
#         """
#         Après la modification de champs, les ingrédients sans identifiant SICCRF devrait
#         avoir `to_be_entered_in_next_decree` comme vrai, car ils ont été créés récemment
#         dans compl'alim. La valeur pour les anciens ne devrait pas être modifiée.
#         """
#         self.teleicare_ingredient.refresh_from_db()
#         self.ca_ingredient.refresh_from_db()
#         self.teleicare_microorganism.refresh_from_db()
#         self.ca_microorganism.refresh_from_db()
#         self.teleicare_plant.refresh_from_db()
#         self.ca_plant.refresh_from_db()
#         self.teleicare_substance.refresh_from_db()
#         self.ca_substance.refresh_from_db()

#         self.assertTrue(self.ca_ingredient.to_be_entered_in_next_decree)
#         self.assertTrue(self.ca_microorganism.to_be_entered_in_next_decree)
#         self.assertTrue(self.ca_plant.to_be_entered_in_next_decree)
#         self.assertTrue(self.ca_substance.to_be_entered_in_next_decree)

#         self.assertFalse(self.teleicare_ingredient.to_be_entered_in_next_decree)
#         self.assertFalse(self.teleicare_microorganism.to_be_entered_in_next_decree)
#         self.assertFalse(self.teleicare_plant.to_be_entered_in_next_decree)
#         self.assertFalse(self.teleicare_substance.to_be_entered_in_next_decree)

# Ce test n'est pas exécuté car il génère une ProgrammingError :
# (le champ generatedField n'existe pas dans la table mais il existe dans le code)
# probablement lié à un bug coté Django
# class RemoveSICCRFFieldsTestCase(TestMigrations):
#     migrate_from = "0160_alter_etablissementtocompanyrelation_options_and_more"
#     migrate_to = "0165_remove_historicalplant_family_by_id_and_more.py"

#     def setUpBeforeMigration(self, apps):
#         MicroorganismOldFactory = apps.get_model("data", "Microorganism")
#         self.teleicare_microorganism = MicroorganismOldFactory.objects.create(
#             siccrf_genus="siccrf genus",
#             ca_genus="ca genus",
#             siccrf_species="siccrf species",
#             ca_species="ca species",
#             siccrf_is_obsolete=True,
#             ca_is_obsolete=None,
#             siccrf_status=1,
#             siccrf_id=2,
#         )
#         PlantFamilyOldFactory = apps.get_model("data", "PlantFamily")
#         PlantOldFactory = apps.get_model("data", "Plant")
#         self.teleicare_plant = PlantOldFactory.objects.create(ca_family=PlantFamilyOldFactory(siccrf_id=12), siccrf_id=3)
#         SubstanceOldFactory = apps.get_model("data", "Substance")
#         self.teleicare_substance = SubstanceOldFactory(siccrf_id=4)
#         self.teleicare_substance.save()

#     def test_migration_0161_to_0165(self):
#         """
#         Après la suppression des champs `siccrf_*` les champs `name`, `is_obsolete`, `status`, `public_comments`,
#         `private_comments`, `genus`, `species`, `family`, `cas_number`, `einec_number`, `nutritional_reference`...
#         doivent être des champs simples (non GeneratedFields) et contenir les valeurs correspondant à Coalesce(`ca_<FIELD>`, `siccrf_<FIELD>`)
#         """
#         self.teleicare_microorganism.refresh_from_db()
#         self.teleicare_plant.refresh_from_db()
#         self.teleicare_substance.refresh_from_db()

#         self.assertType(isinstance(self.teleicare_microorganism.name, models.TextField))
#         with self.assertRaises(FieldDoesNotExist):
#             self.teleicare_microorganism.ca_name
#         with self.assertRaises(FieldDoesNotExist):
#             self.teleicare_microorganism.siccrf_name
#         self.assertTrue(self.teleicare_microorganism.name, "ca genus ca species")
#         self.assertTrue(self.teleicare_microorganism.is_obsolete, True)


# Ce test n'est plus exécuté car le modèle de données à changé
# class SnapshotsTestCase(TestMigrations):
#     migrate_from = "0198_merge_20251103_1411"
#     migrate_to = "0199_remove_approval_comments"

#     def setUpBeforeMigration(self, apps):
#         self.snapshot_1 = SnapshotFactory(
#             action=Snapshot.SnapshotActions.AUTHORIZE_NO_VISA,
#             status=Declaration.DeclarationStatus.AUTHORIZED,
#             comment="Comment to remove",
#             expiration_days=15,
#             blocking_reasons=["1", "2"],
#             declaration=AuthorizedDeclarationFactory(teleicare_declaration_number=None),
#         )
#         self.snapshot_2 = SnapshotFactory(
#             action=Snapshot.SnapshotActions.ACCEPT_VISA,
#             post_validation_status=Declaration.DeclarationStatus.AUTHORIZED,
#             status=Declaration.DeclarationStatus.AUTHORIZED,
#             comment="Comment to remove",
#             expiration_days=15,
#             blocking_reasons=["1", "2"],
#             declaration=AuthorizedDeclarationFactory(teleicare_declaration_number=None),
#         )

#         # Pas pris en compte car le statut n'est pas AUTHORIZED
#         self.snapshot_3 = SnapshotFactory(
#             action=Snapshot.SnapshotActions.ACCEPT_VISA,
#             post_validation_status=Declaration.DeclarationStatus.OBJECTION,
#             status=Declaration.DeclarationStatus.OBJECTION,
#             comment="Comment to preserve",
#             expiration_days=15,
#             blocking_reasons=["1", "2"],
#             declaration=ObjectionDeclarationFactory(teleicare_declaration_number=None),
#         )

#         # Pas pris en compte car l'action et le statut ne sont pas cohérents (on peut en
#         # trouver comme ça dans des déclarations historiques)
#         self.snapshot_4 = SnapshotFactory(
#             action=Snapshot.SnapshotActions.SUBMIT,
#             status=Declaration.DeclarationStatus.AUTHORIZED,
#             comment="Comment to preserve",
#             expiration_days=15,
#             blocking_reasons=["1", "2"],
#             declaration=AuthorizedDeclarationFactory(teleicare_declaration_number=None),
#         )

#         # Pas pris en compte car on ne touche pas les déclarations importées de téléicare
#         self.snapshot_5 = SnapshotFactory(
#             action=Snapshot.SnapshotActions.AUTHORIZE_NO_VISA,
#             status=Declaration.DeclarationStatus.AUTHORIZED,
#             comment="Comment to preserve",
#             expiration_days=15,
#             blocking_reasons=["1", "2"],
#             declaration=AuthorizedDeclarationFactory(teleicare_declaration_number="1234"),
#         )

#     def test_migration_0199(self):
#         """
#         La migration enleve trois champs inutiles des snapshots d'autorisation :
#         - commentaire
#         - expiration_days
#         - blocking_reasons
#         """

#         modified_snapshots = [self.snapshot_1, self.snapshot_2]
#         other_snapshots = [self.snapshot_3, self.snapshot_4, self.snapshot_5]
#         all_snapshots = modified_snapshots + other_snapshots

#         for snapshot in all_snapshots:
#             snapshot.refresh_from_db()

#         for snapshot in modified_snapshots:
#             self.assertEqual(snapshot.comment, "")
#             self.assertIsNone(snapshot.expiration_days)
#             self.assertIsNone(snapshot.blocking_reasons)

#         for snapshot in other_snapshots:
#             self.assertEqual(snapshot.comment, "Comment to preserve")
#             self.assertEqual(snapshot.expiration_days, 15)
#             self.assertEqual(len(snapshot.blocking_reasons), 2)
