from django.test import TestCase

from data.factories import IngredientFactory, MicroorganismFactory, PlantFactory, SubstanceFactory


class IngredientTestCase(TestCase):
    def test_obsolete_ingredients_are_filtered(self):
        """
        Les ingrédients avec la valeur True dans le champ `is_obsolete` ne sont jamais retournés dans les QuerySet
        """
        for ingredient_factory in [SubstanceFactory, IngredientFactory, PlantFactory, MicroorganismFactory]:
            _ = ingredient_factory.create(siccrf_is_obsolete=True, ca_is_obsolete=True)
            non_obsolete_objs = [ingredient_factory.create(ca_is_obsolete=False)]

            qs = ingredient_factory._meta.model.objects.all()
            self.assertQuerySetEqual(qs, non_obsolete_objs, ordered=False)
