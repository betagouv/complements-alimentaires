from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from data.factories import (
    AwaitingInstructionDeclarationFactory,
    ComputedSubstanceFactory,
    DeclaredPlantFactory,
    InstructionReadyDeclarationFactory,
    PlantFactory,
    SnapshotFactory,
    SubstanceFactory,
)
from data.models import Declaration
from data.models.ingredient_status import IngredientStatus


class DeclarationTestCase(TestCase):
    def test_json_representation(self):
        declaration = InstructionReadyDeclarationFactory()
        json_representation = declaration.json_representation

        self.assertEqual(json_representation["id"], declaration.id)
        self.assertEqual(json_representation["status"], declaration.status)
        self.assertEqual(json_representation["author"], declaration.author.id)
        self.assertEqual(json_representation["company"], declaration.company.id)

        json_conditions = json_representation["conditionsNotRecommended"]
        for condition in declaration.conditions_not_recommended.all():
            self.assertIn(condition.id, json_conditions)

        json_populations = json_representation["populations"]
        for population in declaration.populations.all():
            self.assertIn(population.id, json_populations)

        json_effects = json_representation["effects"]
        for effect in declaration.effects.all():
            self.assertIn(effect.id, json_effects)

        json_declared_plants = json_representation["declaredPlants"]
        for declared_plant in declaration.declared_plants.all():
            json_declared_plant = next(filter(lambda x: x["id"] == declared_plant.id, json_declared_plants))
            if declared_plant.plant:
                self.assertEqual(json_declared_plant["element"]["name"], declared_plant.plant.name)
                self.assertEqual(json_declared_plant["element"]["id"], declared_plant.plant.id)
            if declared_plant.used_part:
                self.assertEqual(json_declared_plant["usedPart"], declared_plant.used_part.id)
            if declared_plant.unit:
                self.assertEqual(json_declared_plant["unit"], declared_plant.unit.id)
            self.assertEqual(json_declared_plant["quantity"], declared_plant.quantity)
            self.assertEqual(json_declared_plant["active"], declared_plant.active)

        json_declared_microorganisms = json_representation["declaredMicroorganisms"]
        for declared_microorganism in declaration.declared_microorganisms.all():
            json_declared_microorganism = next(
                filter(lambda x: x["id"] == declared_microorganism.id, json_declared_microorganisms)
            )
            if declared_microorganism.microorganism:
                self.assertEqual(
                    json_declared_microorganism["element"]["name"], declared_microorganism.microorganism.name
                )
                self.assertEqual(json_declared_microorganism["element"]["id"], declared_microorganism.microorganism.id)
            self.assertEqual(json_declared_microorganism["strain"], declared_microorganism.strain)
            self.assertEqual(json_declared_microorganism["quantity"], declared_microorganism.quantity)
            self.assertEqual(json_declared_microorganism["active"], declared_microorganism.active)

        json_declared_ingredients = json_representation["declaredIngredients"]
        for declared_ingredient in declaration.declared_ingredients.all():
            json_declared_ingredient = next(
                filter(lambda x: x["id"] == declared_ingredient.id, json_declared_ingredients)
            )
            if declared_ingredient.ingredient:
                self.assertEqual(json_declared_ingredient["element"]["name"], declared_ingredient.ingredient.name)
                self.assertEqual(json_declared_ingredient["element"]["id"], declared_ingredient.ingredient.id)
            self.assertEqual(json_declared_ingredient["active"], declared_ingredient.active)

        json_declared_substances = json_representation["declaredSubstances"]
        for declared_substance in declaration.declared_substances.all():
            json_declared_substance = next(
                filter(lambda x: x["id"] == declared_substance.id, json_declared_substances)
            )
            if declared_substance.substance:
                self.assertEqual(json_declared_substance["element"]["name"], declared_substance.substance.name)
                self.assertEqual(json_declared_substance["element"]["id"], declared_substance.substance.id)
            self.assertEqual(json_declared_substance["active"], declared_substance.active)

    def test_response_limit_date(self):
        """
        La date limite d'instruction est de deux mois après le dernier changement de statut
        vers "en attente d'instruction"
        """
        declaration = AwaitingInstructionDeclarationFactory()
        snapshot = SnapshotFactory(declaration=declaration, status=declaration.status)

        snapshot.creation_date = timezone.make_aware(datetime(2024, 1, 1, 1, 1, 1, 1))
        snapshot.save()

        response_limit = timezone.make_aware(datetime(2024, 3, 1, 1, 1, 1, 1))
        self.assertEqual(declaration.response_limit_date, response_limit)

    def test_article_empty(self):
        declaration = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )

        declaration.assign_calculated_article()

        self.assertIsNone(declaration.article)
        self.assertEqual(declaration.calculated_article, "")
        self.assertEqual(declaration.overriden_article, "")

    def test_article_15(self):
        declaration = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        DeclaredPlantFactory(new=False, declaration=declaration)
        declaration.assign_calculated_article()
        declaration.save()
        declaration.refresh_from_db()

        self.assertEqual(declaration.article, Declaration.Article.ARTICLE_15)
        self.assertEqual(declaration.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertEqual(declaration.overriden_article, "")

    def test_article_15_override(self):
        declaration = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        # La PlantFactory utilisée dans DeclaredPlantFactory a par défaut un status = AUTHORIZED
        DeclaredPlantFactory(new=False, declaration=declaration)
        declaration.overriden_article = Declaration.Article.ARTICLE_16
        declaration.assign_calculated_article()
        declaration.save()
        declaration.refresh_from_db()

        self.assertEqual(declaration.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertEqual(declaration.overriden_article, Declaration.Article.ARTICLE_16)

    def test_article_16(self):
        """
        Teste si l'article 16 est bien assigné pour :
        - un nouvel ingrédient ajouté
        - un ingrédient non autorisé ajouté
        """
        declaration_new = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        DeclaredPlantFactory(new=True, declaration=declaration_new)
        declaration_new.assign_calculated_article()
        declaration_new.save()
        declaration_new.refresh_from_db()

        self.assertEqual(declaration_new.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_new.calculated_article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_new.overriden_article, "")

        declaration_not_autorized = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        plant_not_autorized = PlantFactory(ca_status=IngredientStatus.NOT_AUTHORIZED)
        DeclaredPlantFactory(plant=plant_not_autorized, declaration=declaration_not_autorized)

        declaration_not_autorized.assign_calculated_article()
        declaration_not_autorized.save()
        declaration_not_autorized.refresh_from_db()

        self.assertEqual(declaration_not_autorized.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_not_autorized.calculated_article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_not_autorized.overriden_article, "")

    def test_article_anses_referal(self):
        declaration = InstructionReadyDeclarationFactory(
            computed_substances=[],
        )
        substance = SubstanceFactory(ca_max_quantity=1.0)
        ComputedSubstanceFactory(
            substance=substance,
            unit=substance.unit,
            quantity=1.2,
            declaration=declaration,
        )
        declaration.assign_calculated_article()
        declaration.save()
        declaration.refresh_from_db()

        self.assertEqual(declaration.article, Declaration.Article.ANSES_REFERAL)
        self.assertEqual(declaration.calculated_article, Declaration.Article.ANSES_REFERAL)
        self.assertEqual(declaration.overriden_article, "")
