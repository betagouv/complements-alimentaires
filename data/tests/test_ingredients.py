from django.test import TestCase
from unittest.mock import patch

from data.factories import (
    DeclaredPlantFactory,
    IngredientFactory,
    MicroorganismFactory,
    OngoingInstructionDeclarationFactory,
    AuthorizedDeclarationFactory,
    PlantFactory,
    PlantPartFactory,
    SubstanceFactory,
)
from data.models.ingredient_type import IngredientType
from data.models.plant import Part
from data.models.substance import SubstanceType
from data.models.declaration import Declaration, Addable


def set_article_15(self):
    self.calculated_article = Declaration.Article.ARTICLE_15


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
        Part.objects.create(plant=plant, plantpart=authorised_part, is_useful=True)
        declaration = OngoingInstructionDeclarationFactory()
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=authorised_part)
        self.assertFalse(declared_plant.is_part_request)

        unauthorised_part = PlantPartFactory()
        Part.objects.create(plant=plant, plantpart=unauthorised_part, is_useful=False)
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=unauthorised_part)
        self.assertTrue(declared_plant.is_part_request)

        unassociated_part = PlantPartFactory()
        self.assertFalse(
            plant.plant_parts.through.objects.filter(plantpart=unassociated_part).exists(),
            "la partie n'est pas associée à la plante",
        )
        declared_plant = DeclaredPlantFactory(declaration=declaration, plant=plant, used_part=unassociated_part)
        self.assertTrue(declared_plant.is_part_request)

    @patch.object(Declaration, "assign_calculated_article", set_article_15)
    def test_added_part_recalculates_ongoing_declaration_article(self):
        """
        Si une partie de plante est demandée, et après elle est ajoutée en dehors du parcours
        primaire, recalculer les articles de déclarations concernées en cours de traitement
        """
        plant = PlantFactory()
        unassociated_part = PlantPartFactory()
        # créer deux déclarations qui devraient être MAJ
        ongoing_declaration_1 = OngoingInstructionDeclarationFactory()
        declared_plant_1 = DeclaredPlantFactory(
            declaration=ongoing_declaration_1, plant=plant, used_part=unassociated_part
        )
        ongoing_declaration_2 = OngoingInstructionDeclarationFactory()
        declared_plant_2 = DeclaredPlantFactory(
            declaration=ongoing_declaration_2, plant=plant, used_part=unassociated_part
        )
        # créer deux déclarations qui ne devraient pas être MAJ
        finished_declaration = AuthorizedDeclarationFactory()
        declared_plant_3 = DeclaredPlantFactory(
            declaration=finished_declaration, plant=plant, used_part=unassociated_part
        )
        no_part_request_declaration = OngoingInstructionDeclarationFactory()

        Part.objects.create(plant=plant, plantpart=unassociated_part, is_useful=True)

        ongoing_declaration_1.refresh_from_db()
        ongoing_declaration_2.refresh_from_db()
        finished_declaration.refresh_from_db()
        no_part_request_declaration.refresh_from_db()

        self.assertEqual(ongoing_declaration_1.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertEqual(ongoing_declaration_2.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertNotEqual(finished_declaration.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertNotEqual(no_part_request_declaration.calculated_article, Declaration.Article.ARTICLE_15)

        declared_plant_1.refresh_from_db()
        declared_plant_2.refresh_from_db()
        declared_plant_3.refresh_from_db()

        self.assertEqual(declared_plant_1.request_status, Addable.AddableStatus.REPLACED)
        self.assertEqual(declared_plant_2.request_status, Addable.AddableStatus.REPLACED)
        self.assertEqual(declared_plant_3.request_status, Addable.AddableStatus.REQUESTED)

    def test_authorised_part_recalculates_ongoing_declaration_article(self):
        """
        Si une partie de plante est demandée, et après elle est autorisée en dehors du parcours
        primare, recalculer les articles de déclarations concernées en cours de traitement
        """
        plant = PlantFactory()
        unauthorised_part = PlantPartFactory()
        part_relation = Part.objects.create(plant=plant, plantpart=unauthorised_part, is_useful=False)
        # créer deux déclarations qui devraient être MAJ
        ongoing_declaration_1 = OngoingInstructionDeclarationFactory()
        declared_plant_1 = DeclaredPlantFactory(
            declaration=ongoing_declaration_1, plant=plant, used_part=unauthorised_part
        )
        ongoing_declaration_2 = OngoingInstructionDeclarationFactory()
        declared_plant_2 = DeclaredPlantFactory(
            declaration=ongoing_declaration_2, plant=plant, used_part=unauthorised_part
        )
        # créer deux déclarations qui ne devraient pas être MAJ
        finished_declaration = AuthorizedDeclarationFactory()
        declared_plant_3 = DeclaredPlantFactory(
            declaration=finished_declaration, plant=plant, used_part=unauthorised_part
        )
        no_part_request_declaration = OngoingInstructionDeclarationFactory()

        part_relation.is_useful = True
        part_relation.save()

        ongoing_declaration_1.refresh_from_db()
        ongoing_declaration_2.refresh_from_db()
        finished_declaration.refresh_from_db()
        no_part_request_declaration.refresh_from_db()

        self.assertEqual(ongoing_declaration_1.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertEqual(ongoing_declaration_2.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertNotEqual(finished_declaration.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertNotEqual(no_part_request_declaration.calculated_article, Declaration.Article.ARTICLE_15)

        declared_plant_1.refresh_from_db()
        declared_plant_2.refresh_from_db()
        declared_plant_3.refresh_from_db()

        self.assertEqual(declared_plant_1.request_status, Addable.AddableStatus.REPLACED)
        self.assertEqual(declared_plant_2.request_status, Addable.AddableStatus.REPLACED)
        self.assertEqual(declared_plant_3.request_status, Addable.AddableStatus.REQUESTED)
