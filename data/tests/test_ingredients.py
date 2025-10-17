from django.test import TestCase

from data.factories import (
    DeclaredPlantFactory,
    IngredientFactory,
    MicroorganismFactory,
    OngoingInstructionDeclarationFactory,
    PlantFactory,
    PlantPartFactory,
    SubstanceFactory,
)
from data.models.ingredient_type import IngredientType
from data.models.plant import Part
from data.models.substance import SubstanceType


class IngredientTestCase(TestCase):
    def test_obsolete_ingredients_are_filtered(self):
        """
        Les ingrédients avec la valeur True dans le champ `is_obsolete` ne sont jamais retournés dans les QuerySet
        """
        for ingredient_factory in [SubstanceFactory, IngredientFactory, PlantFactory, MicroorganismFactory]:
            obsolete_obj = ingredient_factory.create(is_obsolete=True)
            non_obsolete_objs = [ingredient_factory.create(is_obsolete=False) for _ in range(5)]
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
        substance = SubstanceFactory.create(name="substance Z")

        ingredient_supplying_substance = IngredientFactory.create(
            name="substance Z form of supply", ingredient_type=IngredientType.FORM_OF_SUPPLY, substances=[]
        )
        ingredient_supplying_substance.substances.add(substance)
        plant_supplying_substance = PlantFactory.create(name="plant supplying substance Z", substances=[])

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

    def test_declared_plant_auto_assigned_is_part_request_status(self):
        """
        Si une plante déclarée utilise une partie non-autorisée ou non-associée,
        mettre le champ is_part_request à vrai
        """
        plant = PlantFactory()
        authorised_part = PlantPartFactory()
        Part.objects.create(plant=plant, plantpart=authorised_part, status=Part.PartStatus.AUTHORIZED)
        declaration = OngoingInstructionDeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=authorised_part)
        self.assertFalse(declared_plant.is_part_request)

        unauthorised_part = PlantPartFactory()
        Part.objects.create(plant=plant, plantpart=unauthorised_part, status=Part.PartStatus.NOT_AUTHORIZED)
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=unauthorised_part)
        self.assertTrue(declared_plant.is_part_request)

        unassociated_part = PlantPartFactory()
        self.assertFalse(
            plant.plant_parts.through.objects.filter(plantpart=unassociated_part).exists(),
            "la partie n'est pas associée à la plante",
        )
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=unassociated_part)
        self.assertTrue(declared_plant.is_part_request)
