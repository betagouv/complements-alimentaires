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
        Les substances ont leur type calculés correctement
        """
        ose = SubstanceFactory.create(ca_name="pulpose")
        self.assertIn(SubstanceType.CARBOHYDRATE, ose.substance_types)

        ase = SubstanceFactory.create(ca_name="pulpase")
        self.assertIn(SubstanceType.ENZYME, ase.substance_types)

        # une vitamine peut aussi être métabolite
        vitamine = SubstanceFactory.create(ca_name="vitamine Z")

        ingredient_supplying_vitamine = IngredientFactory.create(
            ca_name="vitamine Z supply", ingredient_type=IngredientType.FORM_OF_SUPPLY
        )
        ingredient_supplying_vitamine.substances.add(vitamine)
        plant_supplying_vitamine = PlantFactory.create(ca_name="vitamine Z supply")
        plant_supplying_vitamine.substances.add(vitamine)

        self.assertIn(SubstanceType.VITAMIN, vitamine.substance_types)
        self.assertIn(SubstanceType.SECONDARY_METABOLITE, vitamine.substance_types)

        mineral = SubstanceFactory.create(ca_name="sirum")
        ingredient_supplying_mineral = IngredientFactory.create(
            ca_name="sirum supply", ingredient_type=IngredientType.FORM_OF_SUPPLY, substances=(mineral)
        )
        ingredient_supplying_mineral.substances.add(mineral)

        self.assertIn(SubstanceType.MINERAL, mineral.substance_types)

        nothing = SubstanceFactory.create(ca_name="nothing")
        _ = IngredientFactory.create(
            ca_name="sirum supply", ingredient_type=IngredientType.ACTIVE_INGREDIENT, substances=(nothing)
        )
        self.assertEqual(nothing.substance_types, [])
