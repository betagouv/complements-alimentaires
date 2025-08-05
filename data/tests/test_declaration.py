from datetime import datetime
from random import choice

from django.test import TestCase
from django.utils import timezone

from data.factories import (
    AwaitingInstructionDeclarationFactory,
    ComputedSubstanceFactory,
    DeclarationFactory,
    DeclaredPlantFactory,
    DeclaredSubstanceFactory,
    GalenicFormulationFactory,
    InstructionReadyDeclarationFactory,
    MaxQuantityPerPopulationRelationFactory,
    PlantFactory,
    PlantPartFactory,
    PopulationFactory,
    PreparationFactory,
    SnapshotFactory,
    SubstanceFactory,
)
from data.models import Declaration, Part, Snapshot, SubstanceType
from data.models.ingredient_status import IngredientStatus


class DeclarationTestCase(TestCase):
    def setUp(self):
        self.general_pop = PopulationFactory.create(name="Population générale")

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

    def test_response_limit_date_post_visa(self):
        """
        Un refus de visa ne compte pas dans le calcul du temps limite d'instruction
        """
        declaration = AwaitingInstructionDeclarationFactory()
        snapshot_submission = SnapshotFactory(declaration=declaration, status=declaration.status)
        snapshot_submission.creation_date = timezone.make_aware(datetime(2024, 1, 1, 1, 1, 1, 1))
        snapshot_submission.save()

        snapshot_visa_refuse = SnapshotFactory(
            declaration=declaration, status=declaration.status, action=Snapshot.SnapshotActions.REFUSE_VISA
        )
        snapshot_visa_refuse.creation_date = timezone.make_aware(datetime(2024, 2, 1, 1, 1, 1, 1))
        snapshot_visa_refuse.save()

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
        self.assertEqual(declaration.overridden_article, "")

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
        self.assertEqual(declaration.overridden_article, "")

    def test_article_15_warning(self):
        """
        Il existe 2 types d'article 15 vigilance :
        * la vigilance est liée à la population cible
        * la vigilance est lié à l'ingrédient, ses substances, sa préparation ou la forme galénique du CA
        """
        declaration_with_risky_substance = InstructionReadyDeclarationFactory(
            computed_substances=[],
        )
        substance = SubstanceFactory(is_risky=True)
        ComputedSubstanceFactory(
            substance=substance,
            declaration=declaration_with_risky_substance,
        )
        declaration_with_risky_substance.assign_calculated_article()
        declaration_with_risky_substance.save()
        declaration_with_risky_substance.refresh_from_db()
        self.assertEqual(declaration_with_risky_substance.article, Declaration.Article.ARTICLE_15_WARNING)
        self.assertEqual(declaration_with_risky_substance.calculated_article, Declaration.Article.ARTICLE_15_WARNING)
        self.assertEqual(declaration_with_risky_substance.overridden_article, "")

        declaration_with_risky_prepared_plant = InstructionReadyDeclarationFactory(
            declared_plants=[],
        )
        DeclaredPlantFactory(
            preparation=PreparationFactory(contains_alcohol=True), declaration=declaration_with_risky_prepared_plant
        )
        declaration_with_risky_prepared_plant.assign_calculated_article()
        declaration_with_risky_prepared_plant.save()
        declaration_with_risky_prepared_plant.refresh_from_db()
        self.assertEqual(declaration_with_risky_prepared_plant.article, Declaration.Article.ARTICLE_15_WARNING)
        self.assertEqual(
            declaration_with_risky_prepared_plant.calculated_article, Declaration.Article.ARTICLE_15_WARNING
        )
        self.assertEqual(declaration_with_risky_prepared_plant.overridden_article, "")

        risky_galenic_formulation = GalenicFormulationFactory(is_risky=True)
        declaration_with_risky_galenic_formulation = InstructionReadyDeclarationFactory(
            galenic_formulation=risky_galenic_formulation,
        )

        declaration_with_risky_galenic_formulation.assign_calculated_article()
        declaration_with_risky_galenic_formulation.save()
        declaration_with_risky_galenic_formulation.refresh_from_db()
        self.assertEqual(declaration_with_risky_galenic_formulation.article, Declaration.Article.ARTICLE_15_WARNING)
        self.assertEqual(
            declaration_with_risky_galenic_formulation.calculated_article, Declaration.Article.ARTICLE_15_WARNING
        )
        self.assertEqual(declaration_with_risky_galenic_formulation.overridden_article, "")

        risky_target_population = PopulationFactory(is_defined_by_anses=True)
        declaration_with_risky_population = InstructionReadyDeclarationFactory(
            populations=[risky_target_population],
        )

        declaration_with_risky_population.assign_calculated_article()
        declaration_with_risky_population.save()
        declaration_with_risky_population.refresh_from_db()
        self.assertEqual(
            declaration_with_risky_population.article, Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
        )
        self.assertEqual(
            declaration_with_risky_population.calculated_article, Declaration.Article.ARTICLE_15_HIGH_RISK_POPULATION
        )
        self.assertEqual(declaration_with_risky_population.overridden_article, "")

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
        declaration.overridden_article = Declaration.Article.ARTICLE_16
        declaration.assign_calculated_article()
        declaration.save()
        declaration.refresh_from_db()

        self.assertEqual(declaration.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration.calculated_article, Declaration.Article.ARTICLE_15)
        self.assertEqual(declaration.overridden_article, Declaration.Article.ARTICLE_16)

    def test_article_16(self):
        """
        Teste si l'article 16 est bien assigné pour :
        - un nouvel ingrédient ajouté
        - un ingrédient non autorisé ajouté
        - une partie de plante inconnue
        - une partie de plante non autorisée
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
        self.assertEqual(declaration_new.overridden_article, "")

        declaration_not_autorized = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        plant_not_autorized = PlantFactory(status=IngredientStatus.NOT_AUTHORIZED)
        DeclaredPlantFactory(plant=plant_not_autorized, declaration=declaration_not_autorized)

        declaration_not_autorized.assign_calculated_article()
        declaration_not_autorized.save()
        declaration_not_autorized.refresh_from_db()

        self.assertEqual(declaration_not_autorized.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_not_autorized.calculated_article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_not_autorized.overridden_article, "")

        declaration_part_not_authorized = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        plant_with_part_not_authorized = PlantFactory(status=IngredientStatus.AUTHORIZED)
        plant_part = PlantPartFactory()
        Part.objects.create(plant=plant_with_part_not_authorized, plantpart=plant_part, is_useful=False)

        DeclaredPlantFactory(
            plant=plant_with_part_not_authorized, used_part=plant_part, declaration=declaration_part_not_authorized
        )

        declaration_part_not_authorized.assign_calculated_article()
        declaration_part_not_authorized.save()
        declaration_part_not_authorized.refresh_from_db()

        self.assertEqual(declaration_part_not_authorized.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_part_not_authorized.calculated_article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_part_not_authorized.overridden_article, "")

        declaration_part_unknown = InstructionReadyDeclarationFactory(
            declared_plants=[],
            declared_microorganisms=[],
            declared_substances=[],
            declared_ingredients=[],
            computed_substances=[],
        )
        plant_with_part_unknown = PlantFactory(status=IngredientStatus.AUTHORIZED)
        plant_part = PlantPartFactory()

        DeclaredPlantFactory(plant=plant_with_part_unknown, used_part=plant_part, declaration=declaration_part_unknown)

        declaration_part_unknown.assign_calculated_article()
        declaration_part_unknown.save()
        declaration_part_unknown.refresh_from_db()

        self.assertEqual(declaration_part_unknown.article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_part_unknown.calculated_article, Declaration.Article.ARTICLE_16)
        self.assertEqual(declaration_part_unknown.overridden_article, "")

    def test_article_18(self):
        SUBSTANCE_MAX_QUANTITY = 1.0

        substance_types = [
            [SubstanceType.VITAMIN],
            [SubstanceType.MINERAL],
            [SubstanceType.BIOACTIVE_SUBSTANCE, SubstanceType.MINERAL],
            [SubstanceType.SECONDARY_METABOLITE, SubstanceType.VITAMIN],
        ]
        for type in substance_types:
            declaration_with_computed_nutriment_max_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[]
            )

            substance = SubstanceFactory(substance_types=type)
            MaxQuantityPerPopulationRelationFactory(
                substance=substance,
                population=self.general_pop,
                max_quantity=SUBSTANCE_MAX_QUANTITY,
            )
            ComputedSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=1.2,
                declaration=declaration_with_computed_nutriment_max_exceeded,
            )
            declaration_with_computed_nutriment_max_exceeded.assign_calculated_article()
            declaration_with_computed_nutriment_max_exceeded.save()
            declaration_with_computed_nutriment_max_exceeded.refresh_from_db()
            self.assertEqual(declaration_with_computed_nutriment_max_exceeded.article, Declaration.Article.ARTICLE_18)
            self.assertEqual(
                declaration_with_computed_nutriment_max_exceeded.calculated_article, Declaration.Article.ARTICLE_18
            )
            self.assertEqual(declaration_with_computed_nutriment_max_exceeded.overridden_article, "")

            # La déclaration ne doit pas passer en saisine ANSES si la dose est exactement égale à la dose maximale
            declaration_with_computed_nutriment_equals_max = InstructionReadyDeclarationFactory(
                computed_substances=[],
            )
            ComputedSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=SUBSTANCE_MAX_QUANTITY,
                declaration=declaration_with_computed_nutriment_equals_max,
            )
            declaration_with_computed_nutriment_equals_max.assign_calculated_article()
            declaration_with_computed_nutriment_equals_max.save()
            declaration_with_computed_nutriment_equals_max.refresh_from_db()
            self.assertEqual(declaration_with_computed_nutriment_equals_max.article, Declaration.Article.ARTICLE_15)
            self.assertEqual(
                declaration_with_computed_nutriment_equals_max.calculated_article, Declaration.Article.ARTICLE_15
            )
            self.assertEqual(declaration_with_computed_nutriment_equals_max.overridden_article, "")

            declaration_with_declared_nutriment_max_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[],
            )
            DeclaredSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=1.2,
                declaration=declaration_with_declared_nutriment_max_exceeded,
            )
            declaration_with_declared_nutriment_max_exceeded.assign_calculated_article()
            declaration_with_declared_nutriment_max_exceeded.save()
            declaration_with_declared_nutriment_max_exceeded.refresh_from_db()
            self.assertEqual(declaration_with_declared_nutriment_max_exceeded.article, Declaration.Article.ARTICLE_18)
            self.assertEqual(
                declaration_with_declared_nutriment_max_exceeded.calculated_article, Declaration.Article.ARTICLE_18
            )
            self.assertEqual(declaration_with_declared_nutriment_max_exceeded.overridden_article, "")

    def test_article_anses_referal_for_general_population(self):
        """
        Une déclaration doit passer en article `ANSES_REFERAL` si :
        * la dose max d'une substance déclarée est dépassée pour la population générale
        * la dose max d'une substance calculée est dépassée pour la population générale
        """
        SUBSTANCE_MAX_QUANTITY = 1.0
        substance_types = [
            [SubstanceType.SECONDARY_METABOLITE],
            [SubstanceType.BIOACTIVE_SUBSTANCE],
            [SubstanceType.SECONDARY_METABOLITE, SubstanceType.BIOACTIVE_SUBSTANCE],
            [],
        ]
        for type in substance_types:
            declaration_with_computed_substance_max_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[], populations=[self.general_pop]
            )
            substance = SubstanceFactory(substance_types=type)
            MaxQuantityPerPopulationRelationFactory(
                substance=substance,
                population=self.general_pop,
                max_quantity=SUBSTANCE_MAX_QUANTITY,
            )
            ComputedSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=1.2,
                declaration=declaration_with_computed_substance_max_exceeded,
            )
            declaration_with_computed_substance_max_exceeded.assign_calculated_article()
            declaration_with_computed_substance_max_exceeded.save()
            declaration_with_computed_substance_max_exceeded.refresh_from_db()
            self.assertEqual(
                declaration_with_computed_substance_max_exceeded.article, Declaration.Article.ANSES_REFERAL
            )
            self.assertEqual(
                declaration_with_computed_substance_max_exceeded.calculated_article, Declaration.Article.ANSES_REFERAL
            )
            self.assertEqual(declaration_with_computed_substance_max_exceeded.overridden_article, "")

            # La déclaration ne doit pas passer en saisine ANSES si la dose est exactement égale à la dose maximale
            declaration_with_computed_substance_equals_max = InstructionReadyDeclarationFactory(
                computed_substances=[],
            )
            ComputedSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=SUBSTANCE_MAX_QUANTITY,
                declaration=declaration_with_computed_substance_equals_max,
            )
            declaration_with_computed_substance_equals_max.assign_calculated_article()
            declaration_with_computed_substance_equals_max.save()
            declaration_with_computed_substance_equals_max.refresh_from_db()
            self.assertEqual(declaration_with_computed_substance_equals_max.article, Declaration.Article.ARTICLE_15)
            self.assertEqual(
                declaration_with_computed_substance_equals_max.calculated_article, Declaration.Article.ARTICLE_15
            )
            self.assertEqual(declaration_with_computed_substance_equals_max.overridden_article, "")

            declaration_with_declared_substance_max_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[],
            )
            DeclaredSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=1.2,
                declaration=declaration_with_declared_substance_max_exceeded,
            )
            declaration_with_declared_substance_max_exceeded.assign_calculated_article()
            declaration_with_declared_substance_max_exceeded.save()
            declaration_with_declared_substance_max_exceeded.refresh_from_db()
            self.assertEqual(
                declaration_with_declared_substance_max_exceeded.article, Declaration.Article.ANSES_REFERAL
            )
            self.assertEqual(
                declaration_with_declared_substance_max_exceeded.calculated_article, Declaration.Article.ANSES_REFERAL
            )
            self.assertEqual(declaration_with_declared_substance_max_exceeded.overridden_article, "")

    def test_all_populations_are_considered_for_article_assignation(self):
        """
        Les substances qui ont une doses maximum pour une population autre
        que la population générale doivent être considérées comme dépassées
        si elles font partie des populations cibles
        """
        pop_biggest_quantity = PopulationFactory(name="Population extradosée")
        pop_smallest_quantity = PopulationFactory(name="Population microdosée")
        pop_no_quantity = PopulationFactory(name="Population sans indication")
        nutriment_type = choice([[SubstanceType.VITAMIN], [SubstanceType.MINERAL]])
        other_substance_type = choice(
            [
                [SubstanceType.SECONDARY_METABOLITE],
                [SubstanceType.BIOACTIVE_SUBSTANCE],
                [SubstanceType.SECONDARY_METABOLITE, SubstanceType.BIOACTIVE_SUBSTANCE],
                [],
            ]
        )
        for substance_type in [
            nutriment_type,
            other_substance_type,
        ]:
            substance = SubstanceFactory(substance_types=substance_type)
            MaxQuantityPerPopulationRelationFactory(
                substance=substance,
                population=self.general_pop,
                max_quantity=2,
            )
            MaxQuantityPerPopulationRelationFactory(
                substance=substance,
                population=pop_smallest_quantity,
                max_quantity=1,
            )
            MaxQuantityPerPopulationRelationFactory(
                substance=substance,
                population=pop_biggest_quantity,
                max_quantity=10,
            )
            declaration_max_quantity_for_general_pop_not_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[],
            )
            DeclaredSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=1.2,
                declaration=declaration_max_quantity_for_general_pop_not_exceeded,
            )
            declaration_max_quantity_for_general_pop_not_exceeded.assign_calculated_article()
            declaration_max_quantity_for_general_pop_not_exceeded.save()
            declaration_max_quantity_for_general_pop_not_exceeded.refresh_from_db()
            self.assertEqual(
                declaration_max_quantity_for_general_pop_not_exceeded.article,
                Declaration.Article.ARTICLE_15,
                "Une déclaration sans population cible et dont la quantité de substance ne dépasse pas la dose max pour la population générale passe en article 15",
            )
            declaration_with_max_quantity_specific_pop_not_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[], populations=[pop_biggest_quantity]
            )
            DeclaredSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=10,
                declaration=declaration_with_max_quantity_specific_pop_not_exceeded,
            )
            declaration_with_max_quantity_specific_pop_not_exceeded.assign_calculated_article()
            declaration_with_max_quantity_specific_pop_not_exceeded.save()
            declaration_with_max_quantity_specific_pop_not_exceeded.refresh_from_db()
            self.assertEqual(
                declaration_with_max_quantity_specific_pop_not_exceeded.article,
                Declaration.Article.ARTICLE_15,
                "Une déclaration avec population cible et dont la quantité de substance ne dépasse pas la dose max pour cette population cible passe en article 15",
            )
            declaration_with_max_quantity_specific_pop_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[], populations=[pop_biggest_quantity, pop_smallest_quantity]
            )
            DeclaredSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=10,
                declaration=declaration_with_max_quantity_specific_pop_exceeded,
            )
            declaration_with_max_quantity_specific_pop_exceeded.assign_calculated_article()
            declaration_with_max_quantity_specific_pop_exceeded.save()
            declaration_with_max_quantity_specific_pop_exceeded.refresh_from_db()
            if substance.substance_types == other_substance_type:
                self.assertEqual(
                    declaration_with_max_quantity_specific_pop_exceeded.article,
                    Declaration.Article.ANSES_REFERAL,
                    "Une déclaration avec plusieurs population cible, passe en article ANSES_REFERAL si la plus petite des max_quantity des population cibles est dépassée pour une substance non vitamine et minéraux",
                )
            else:
                self.assertEqual(
                    declaration_with_max_quantity_specific_pop_exceeded.article,
                    Declaration.Article.ARTICLE_18,
                    "Une déclaration avec plusieurs population cible, passe en ARTICLE_18 si la plus petite des max_quantity des population cibles est dépassée pour un nutriment",
                )
            declaration_with_max_quantity_general_pop_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[],
            )
            DeclaredSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=10,
                declaration=declaration_with_max_quantity_general_pop_exceeded,
            )
            declaration_with_max_quantity_general_pop_exceeded.assign_calculated_article()
            declaration_with_max_quantity_general_pop_exceeded.save()
            declaration_with_max_quantity_general_pop_exceeded.refresh_from_db()
            if substance.substance_types == other_substance_type:
                self.assertEqual(
                    declaration_with_max_quantity_general_pop_exceeded.article,
                    Declaration.Article.ANSES_REFERAL,
                    "Une déclaration sans population cible, passe en article ANSES_REFERAL si la max_quantity pour la population générale est dépassée pour un nutriment",
                )
            else:
                self.assertEqual(
                    declaration_with_max_quantity_general_pop_exceeded.article,
                    Declaration.Article.ARTICLE_18,
                    "Une déclaration sans population cible, passe en ARTICLE_18 si la max_quantity pour la population générale est dépassée pour un nutriment",
                )
            declaration_with_specific_pop_max_quantity_general_pop_exceeded = InstructionReadyDeclarationFactory(
                computed_substances=[], populations=[pop_no_quantity, pop_biggest_quantity]
            )
            DeclaredSubstanceFactory(
                substance=substance,
                unit=substance.unit,
                quantity=3,
                declaration=declaration_with_specific_pop_max_quantity_general_pop_exceeded,
            )
            declaration_with_specific_pop_max_quantity_general_pop_exceeded.assign_calculated_article()
            declaration_with_specific_pop_max_quantity_general_pop_exceeded.save()
            declaration_with_specific_pop_max_quantity_general_pop_exceeded.refresh_from_db()
            if substance.substance_types == other_substance_type:
                self.assertEqual(
                    declaration_with_specific_pop_max_quantity_general_pop_exceeded.article,
                    Declaration.Article.ANSES_REFERAL,
                    "Une déclaration avec une population cible sans dose max, passe en article ANSES_REFERAL si la quantité por la population générale est dépassée pour une substance non vitamine et minéraux",
                )
            else:
                self.assertEqual(
                    declaration_with_specific_pop_max_quantity_general_pop_exceeded.article,
                    Declaration.Article.ARTICLE_18,
                    "Une déclaration avec une population cible sans dose max, passe en ARTICLE_18 si la quantité por la population générale est dépassée pour un nutriment",
                )

    def test_visa_refused(self):
        """
        La propriété `visa_refused` est présente si le visa a été refusé et qu'aucune action
        du pro a été effectué depuis.
        """
        # Une déclaration en draft ne doit pas être visa_refused
        declaration = DeclarationFactory()
        self.assertFalse(declaration.visa_refused)

        # On soumet la déclaration
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.SUBMIT,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
        )
        declaration.status = Declaration.DeclarationStatus.AWAITING_INSTRUCTION
        declaration.save()
        self.assertFalse(declaration.visa_refused)

        # On demande le visa
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.REQUEST_VISA,
            status=Declaration.DeclarationStatus.AWAITING_VISA,
        )
        declaration.status = Declaration.DeclarationStatus.AWAITING_VISA
        declaration.save()
        self.assertFalse(declaration.visa_refused)

        # On refuse le visa - visa_refused doit être à true
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.REFUSE_VISA,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
        )
        declaration.status = Declaration.DeclarationStatus.AWAITING_INSTRUCTION
        declaration.save()
        self.assertTrue(declaration.visa_refused)

        # Si une instructrice s'assigne le dossier - visa_refused doit être toujours à true
        # car on n'a pas eu une réponse du pro
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.TAKE_FOR_INSTRUCTION,
            status=Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
        )
        declaration.status = Declaration.DeclarationStatus.ONGOING_INSTRUCTION
        declaration.save()
        self.assertTrue(declaration.visa_refused)

        # En faisant une observation, le dossier repasse côté pro, donc on revient à false
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.OBSERVE_NO_VISA,
            status=Declaration.DeclarationStatus.OBSERVATION,
        )
        declaration.status = Declaration.DeclarationStatus.OBSERVATION
        declaration.save()
        self.assertFalse(declaration.visa_refused)

        # Si le ou la pro répond à l'observation, visa_refused reste false
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
        )
        declaration.status = Declaration.DeclarationStatus.AWAITING_INSTRUCTION
        declaration.save()
        self.assertFalse(declaration.visa_refused)

    def test_pending_pro_responses(self):
        """
        On vérifie si une déclaration côté instruction a déjà fait un aller-retour
        côté pro, çad si le pro a déjà répondu une remarque de l'administration.
        """
        # Une déclaration en draft ne doit pas être has_pending_pro_responses
        declaration = DeclarationFactory()
        self.assertFalse(declaration.has_pending_pro_responses)

        # On soumet la déclaration
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.SUBMIT,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
        )
        declaration.status = Declaration.DeclarationStatus.AWAITING_INSTRUCTION
        declaration.save()
        self.assertFalse(declaration.has_pending_pro_responses)

        # En faisant une observation, le dossier repasse côté pro.
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.OBSERVE_NO_VISA,
            status=Declaration.DeclarationStatus.OBSERVATION,
        )
        declaration.status = Declaration.DeclarationStatus.OBSERVATION
        declaration.save()
        self.assertFalse(declaration.has_pending_pro_responses)

        # Si le ou la pro répond à l'observation, has_pending_pro_responses passe à true
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.RESPOND_TO_OBSERVATION,
            status=Declaration.DeclarationStatus.AWAITING_INSTRUCTION,
        )
        declaration.status = Declaration.DeclarationStatus.AWAITING_INSTRUCTION
        declaration.save()
        self.assertTrue(declaration.has_pending_pro_responses)

        # Quand l'instructrice s'assigne le dossier, has_pending_pro_responses reste à true
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.TAKE_FOR_INSTRUCTION,
            status=Declaration.DeclarationStatus.ONGOING_INSTRUCTION,
        )
        declaration.status = Declaration.DeclarationStatus.ONGOING_INSTRUCTION
        declaration.save()
        self.assertTrue(declaration.has_pending_pro_responses)

        # En refaisant une observation, has_pending_pro_responses repasse à false
        SnapshotFactory(
            declaration=declaration,
            action=Snapshot.SnapshotActions.OBSERVE_NO_VISA,
            status=Declaration.DeclarationStatus.OBSERVATION,
        )
        declaration.status = Declaration.DeclarationStatus.OBSERVATION
        declaration.save()
        self.assertFalse(declaration.has_pending_pro_responses)
