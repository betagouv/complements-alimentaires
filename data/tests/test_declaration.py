from django.test import TestCase

from data.factories import InstructionReadyDeclarationFactory


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
