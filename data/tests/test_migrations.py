from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase

from data.factories import IngredientFactory, MicroorganismFactory, PlantFactory, SubstanceFactory


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


class ApproFieldsTestCase(TestMigrations):
    migrate_from = "0149_alter_declaration_teleicare_id_and_more"
    migrate_to = "0150_alter_historicalingredient_to_be_entered_in_next_decree_and_more"

    def setUpBeforeMigration(self, apps):
        self.teleicare_ingredient = IngredientFactory.create(siccrf_id=1, to_be_entered_in_next_decree=False)
        self.ca_ingredient = IngredientFactory.create(siccrf_id=None, to_be_entered_in_next_decree=False)
        self.teleicare_microorganism = MicroorganismFactory.create(siccrf_id=2, to_be_entered_in_next_decree=False)
        self.ca_microorganism = MicroorganismFactory.create(siccrf_id=None, to_be_entered_in_next_decree=False)
        self.teleicare_plant = PlantFactory.create(siccrf_id=3, to_be_entered_in_next_decree=False)
        self.ca_plant = PlantFactory.create(siccrf_id=None, to_be_entered_in_next_decree=False)
        self.teleicare_substance = SubstanceFactory.create(siccrf_id=4, to_be_entered_in_next_decree=False)
        self.ca_substance = SubstanceFactory.create(siccrf_id=None, to_be_entered_in_next_decree=False)

    def test_migration_0150(self):
        """
        Après la modification de champs, les ingrédients sans identifiant SICCRF devrait
        avoir `to_be_entered_in_next_decree` comme vrai, car ils ont été créés récemment
        dans compl'alim. La valeur pour les anciens ne devrait pas être modifiée.
        """
        self.teleicare_ingredient.refresh_from_db()
        self.ca_ingredient.refresh_from_db()
        self.teleicare_microorganism.refresh_from_db()
        self.ca_microorganism.refresh_from_db()
        self.teleicare_plant.refresh_from_db()
        self.ca_plant.refresh_from_db()
        self.teleicare_substance.refresh_from_db()
        self.ca_substance.refresh_from_db()

        self.assertTrue(self.ca_ingredient.to_be_entered_in_next_decree)
        self.assertTrue(self.ca_microorganism.to_be_entered_in_next_decree)
        self.assertTrue(self.ca_plant.to_be_entered_in_next_decree)
        self.assertTrue(self.ca_substance.to_be_entered_in_next_decree)

        self.assertFalse(self.teleicare_ingredient.to_be_entered_in_next_decree)
        self.assertFalse(self.teleicare_microorganism.to_be_entered_in_next_decree)
        self.assertFalse(self.teleicare_plant.to_be_entered_in_next_decree)
        self.assertFalse(self.teleicare_substance.to_be_entered_in_next_decree)
