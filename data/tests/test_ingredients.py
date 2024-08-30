from django.test import TestCase

from data.factories import IngredientFactory, MicroorganismFactory, PlantFactory, SubstanceFactory


class IngredientTestCase(TestCase):
    def test_obsolete_ingredients_are_filtered(self):
        """
        Les ingrédients avec la valeur True dans le champ `is_obsolete` ne sont jamais retournés dans les QuerySet
        """
        for ingredient_factory in [SubstanceFactory, IngredientFactory, PlantFactory, MicroorganismFactory]:
            obsolete_obj = ingredient_factory.create(siccrf_is_obsolete=True, ca_is_obsolete=True)
            non_obsolete_objs = [
                ingredient_factory.create(ca_is_obsolete=False, siccrf_is_obsolete=False) for _ in range(5)
            ]
            all_objs = non_obsolete_objs + [obsolete_obj]

            qs_without_obsolete = ingredient_factory._meta.model.objects.all()
            self.assertQuerySetEqual(qs_without_obsolete, non_obsolete_objs, ordered=False)
            qs_with_obsolete = ingredient_factory._meta.model.all_objects.all()
            self.assertQuerySetEqual(qs_with_obsolete, all_objs, ordered=False)
