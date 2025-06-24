from django.test import TestCase

from data.factories import (
    IngredientFactory,
    MicroorganismFactory,
    PlantFactory,
    SubstanceFactory,
    PlantPartFactory,
    DeclaredPlantFactory,
    OngoingInstructionDeclarationFactory,
)
from data.models.ingredient_type import IngredientType
from data.models.substance import SubstanceType
from data.models.plant import Part


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

    def test_declared_plant_auto_assigned_is_part_request_status(self):
        """
        Si une plante déclarée utilise une partie non-autorisée ou non-associée,
        mettre le champ is_part_request à vrai
        """
        plant = PlantFactory()
        authorised_part = PlantPartFactory()
        Part.objects.create(plant=plant, plantpart=authorised_part, ca_is_useful=True)
        declaration = OngoingInstructionDeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=authorised_part)
        self.assertFalse(declared_plant.is_part_request)

        unauthorised_part = PlantPartFactory()
        Part.objects.create(plant=plant, plantpart=unauthorised_part, ca_is_useful=False)
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=unauthorised_part)
        self.assertTrue(declared_plant.is_part_request)

        unassociated_part = PlantPartFactory()
        self.assertFalse(
            plant.plant_parts.through.objects.filter(plantpart=unassociated_part).exists(),
            "la partie n'est pas associée à la plante",
        )
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=unassociated_part)
        self.assertTrue(declared_plant.is_part_request)

    # def test_declared_plant_is_part_request_status_updated_with_deauthorisation(self):
    #     """
    #     Si une partie est de-autorisée, il faut mettre is_part_request à vrai
    #     """
    #     plant = PlantFactory()
    #     authorised_part = PlantPartFactory()
    #     authorised_plant_part = Part.objects.create(plant=plant, plantpart=authorised_part, ca_is_useful=True)
    #     declared_plant = DeclaredPlantFactory(
    #         declaration=OngoingInstructionDeclarationFactory(), plant=plant, used_part=authorised_part
    #     )
    #     self.assertFalse(declared_plant.is_part_request, "is_part_request n'est pas cochée pour les parties autorisées")

    #     authorised_plant_part.ca_is_useful = False
    #     authorised_plant_part.save()
    #     declared_plant.refresh_from_db()
    #     self.assertTrue(declared_plant.is_part_request)

    # def test_declared_plant_is_part_request_status_updated_with_authorisation(self):
    #     """
    #     Si une partie est autorisée, il faut mettre is_part_request à faux
    #     """
    #     plant = PlantFactory()
    #     unauthorised_part = PlantPartFactory()
    #     unauthorised_plant_part = Part.objects.create(plant=plant, plantpart=unauthorised_part, ca_is_useful=False)
    #     declared_plant = DeclaredPlantFactory(
    #         declaration=OngoingInstructionDeclarationFactory(), plant=plant, used_part=unauthorised_part
    #     )
    #     self.assertTrue(declared_plant.is_part_request, "is_part_request est cochée pour les parties non-autorisées")

    #     unauthorised_plant_part.ca_is_useful = True
    #     unauthorised_plant_part.save()
    #     declared_plant.refresh_from_db()
    #     self.assertFalse(declared_plant.is_part_request)

    # def test_declared_plant_is_part_request_status_updated_with_deletion(self):
    #     """
    #     Si une partie est supprimée, il faut mettre is_part_request à True
    #     """
    #     plant = PlantFactory()
    #     authorised_part = PlantPartFactory()
    #     authorised_plant_part = Part.objects.create(plant=plant, plantpart=authorised_part, ca_is_useful=True)
    #     declared_plant = DeclaredPlantFactory(
    #         declaration=OngoingInstructionDeclarationFactory(), plant=plant, used_part=authorised_part
    #     )

    #     authorised_plant_part.delete()
    #     declared_plant.refresh_from_db()
    #     self.assertTrue(declared_plant.is_part_request)

    # def test_declared_plant_is_part_request_status_updated_with_addition(self):
    #     """
    #     Si une partie est ajoutée, il faut mettre is_part_request à True si autorisée et garder à faux sinon
    #     """
    #     plant = PlantFactory()
    #     unknown_part = PlantPartFactory()
    #     self.assertFalse(
    #         plant.plant_parts.through.objects.filter(plantpart=unknown_part).exists(),
    #         "la partie n'est pas associée à la plante",
    #     )
    #     declared_plant = DeclaredPlantFactory(
    #         declaration=OngoingInstructionDeclarationFactory(), plant=plant, used_part=unknown_part
    #     )
    #     self.assertTrue(declared_plant.is_part_request)

    #     # test : crée mais non-autorisée
    #     newly_authorised_plant_part = Part.objects.create(plant=plant, plantpart=unknown_part, ca_is_useful=True)
    #     declared_plant.refresh_from_db()
    #     self.assertFalse(declared_plant.is_part_request)

    #     newly_authorised_plant_part.delete()
    #     # test: crée et autorisée
    #     newly_authorised_plant_part = Part.objects.create(plant=plant, plantpart=unknown_part, ca_is_useful=False)
    #     declared_plant.refresh_from_db()
    #     self.assertTrue(declared_plant.is_part_request)
