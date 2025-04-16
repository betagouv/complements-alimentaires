from django.test import TestCase

from data.factories import IngredientFactory, MicroorganismFactory, PlantFactory, SubstanceFactory
from data.models.ingredient_type import IngredientType
from data.models.substance import SubstanceType


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

            qs_without_obsolete = ingredient_factory._meta.model.up_to_date_objects.all()
            self.assertQuerySetEqual(qs_without_obsolete, non_obsolete_objs, ordered=False)
            qs_with_obsolete = ingredient_factory._meta.model.objects.all()
            self.assertQuerySetEqual(qs_with_obsolete, all_objs, ordered=False)

    def test_substance_types_are_well_assigned(self):
        """
        Les substances ont le type métabolite secondaire calculé automatiquement correctement
        """
        # une substance peut être métabolite et un autre type
        substance = SubstanceFactory.create(ca_name="substance Z")

        ingredient_supplying_substance = IngredientFactory.create(
            ca_name="substance Z form of supply", ingredient_type=IngredientType.FORM_OF_SUPPLY, substances=[]
        )
        ingredient_supplying_substance.substances.add(substance)
        plant_supplying_substance = PlantFactory.create(ca_name="plant supplying substance Z", substances=[])

        plant_supplying_substance.substances.add(substance)
        substance.refresh_from_db()
        self.assertIn(SubstanceType.SECONDARY_METABOLITE, substance.substance_types)

        # une substance n'est plus métabolite si elle n'est plus rattachée à une plante
        # la substance est retirée de la plante
        plant_supplying_substance.substances.remove(substance)
        substance.refresh_from_db()
        self.assertNotIn(SubstanceType.SECONDARY_METABOLITE, substance.substance_types)
        # la plante est retirée de la substance (le signal fonctionne dans les deux sens de la relation)
        substance.plant_set.add(plant_supplying_substance)
        substance.refresh_from_db()
        self.assertIn(SubstanceType.SECONDARY_METABOLITE, substance.substance_types)
        substance.plant_set.remove(plant_supplying_substance)
        substance.refresh_from_db()
        self.assertNotIn(SubstanceType.SECONDARY_METABOLITE, substance.substance_types)
