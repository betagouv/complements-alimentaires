from django.urls import reverse

from rest_framework.test import APITestCase

from data.factories import (
    AuthorizedDeclarationFactory,
    ComputedSubstanceFactory,
    DeclaredIngredientFactory,
    DeclaredMicroorganismFactory,
    DeclaredPlantFactory,
    IngredientFactory,
    InstructionRoleFactory,
    MicroorganismFactory,
    PlantFactory,
    PlantPartFactory,
    SubstanceFactory,
    SubstanceUnitFactory,
)

from .utils import authenticate


class DeclarationDoseFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Utilisé au lieu de setUp car on ne modifie pas la donnée, donc c'est mieux si ces
        # objets sont créés seulement une fois.

        cls.unit_mg = SubstanceUnitFactory(name="mg")
        cls.unit_g = SubstanceUnitFactory(name="g")

        cls.camomille = PlantFactory(name="Camomille")
        cls.mint = PlantFactory(name="Mint")
        cls.branch = PlantPartFactory(name="Branch")
        cls.leaf = PlantPartFactory(name="Leaf")

        cls.caffeine = SubstanceFactory(name="Caffeine")
        cls.vitamin_c = SubstanceFactory(name="Vitamin C")

        cls.lactobacillus = MicroorganismFactory(genus="Lactobacillus", species="bulgaricus")
        cls.bifidobacterium = MicroorganismFactory(genus="Bifidobacterium", species="jbl")

        cls.green_tea = IngredientFactory(name="Green Tea Extract")
        cls.ginger = IngredientFactory(name="Ginger Root")

        cls.declaration1 = AuthorizedDeclarationFactory()
        DeclaredPlantFactory(
            declaration=cls.declaration1, plant=cls.camomille, used_part=cls.branch, quantity=5.0, unit=cls.unit_mg
        )

        cls.declaration2 = AuthorizedDeclarationFactory()
        ComputedSubstanceFactory(declaration=cls.declaration2, substance=cls.caffeine, quantity=12.5, unit=cls.unit_mg)

        cls.declaration3 = AuthorizedDeclarationFactory()
        DeclaredMicroorganismFactory(declaration=cls.declaration3, microorganism=cls.lactobacillus, quantity=1000000)

        cls.declaration4 = AuthorizedDeclarationFactory()
        DeclaredIngredientFactory(
            declaration=cls.declaration4, ingredient=cls.green_tea, quantity=0.5, unit=cls.unit_g
        )

        cls.declaration5 = AuthorizedDeclarationFactory()
        DeclaredPlantFactory(
            declaration=cls.declaration5, plant=cls.mint, used_part=cls.leaf, quantity=10.0, unit=cls.unit_mg
        )
        ComputedSubstanceFactory(
            declaration=cls.declaration5, substance=cls.vitamin_c, quantity=80.0, unit=cls.unit_mg
        )

    def make_request(self, dose_string):
        url = f"{reverse('api:list_all_declarations')}?{dose_string}"
        response = self.client.get(url, format="json")
        return response.json()["results"]

    @authenticate
    def test_filter_plant_dose_greater_than(self):
        """Test filtering declarations with plant dose greater than specified value"""
        InstructionRoleFactory(user=authenticate.user)
        dose = f"dose=plant||Camomille||{self.camomille.id}|{self.branch.id}|Branch||>||4||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration1.id)

    @authenticate
    def test_filter_substance_dose_between(self):
        """Test filtering declarations with substance dose between two values"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=substance||Caffeine||{self.caffeine.id}||≬||10|15||{self.unit_mg.id}")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration2.id)

    @authenticate
    def test_filter_microorganism_dose_less_than_or_equal(self):
        """Test filtering declarations with microorganism dose less than or equal to specified value"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=microorganism||Lactobacillus||{self.lactobacillus.id}||≤||1000000")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration3.id)

    @authenticate
    def test_filter_plant_dose_without_part(self):
        """Test filtering declarations with plant dose without specifying plant part"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=plant||Mint||{self.mint.id}||≥||10||{self.unit_mg.id}")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration5.id)

    @authenticate
    def test_filter_with_multiple_criteria(self):
        """Test that declarations must match all filter criteria"""
        InstructionRoleFactory(user=authenticate.user)
        # Rien ne devrait être trouvé car declaration5 a mint >= 10mg mais vitamin_c is 80mg (pas entre 90-100)
        dose = f"dose=plant||Mint||{self.mint.id}||≥||10||{self.unit_mg.id}&dose=substance||Vitamin C||{self.vitamin_c.id}||≬||90|100||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 0)

    @authenticate
    def test_invalid_dose_format(self):
        """Test that invalid dose format returns no results"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request("dose=invalid_format")
        self.assertEqual(len(results), 0)

    @authenticate
    def test_nonexistent_element(self):
        """Test filtering with non-existent element ID returns no results"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=plant||Nonexistent||999||≥||10||{self.unit_mg.id}")
        self.assertEqual(len(results), 0)
