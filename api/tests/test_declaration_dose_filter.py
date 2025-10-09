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
    UnitFactory,
)
from data.models import IngredientType

from .utils import authenticate


class DeclarationDoseFilterTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Utilisé au lieu de setUp car on ne modifie pas la donnée, donc c'est mieux si ces
        # objets sont créés seulement une fois.

        cls.unit_mg = UnitFactory(name="mg")
        cls.unit_g = UnitFactory(name="g")

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
        """Filtrage par dose d'une plante supérieure à une certaine valeur"""
        InstructionRoleFactory(user=authenticate.user)
        dose = f"dose=plant||Camomille||{self.camomille.id}|{self.branch.id}|Branch||>||4||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration1.id)

    @authenticate
    def test_filter_substance_dose_between(self):
        """Filtrage d'une dose d'une substance entre deux valeurs"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=substance||Caffeine||{self.caffeine.id}||≬||10|15||{self.unit_mg.id}")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration2.id)

    @authenticate
    def test_filter_microorganism_dose_less_than_or_equal(self):
        """Filtrage d'un micro-organisme inférieur ou égal à une valeur"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=microorganism||Lactobacillus||{self.lactobacillus.id}||≤||1000000")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration3.id)

    @authenticate
    def test_filter_plant_dose_without_part(self):
        """Filtrage de dose pour une plante sans spécifier une partie de plante"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=plant||Mint||{self.mint.id}||≥||10||{self.unit_mg.id}")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration5.id)

    @authenticate
    def test_filter_with_multiple_criteria(self):
        """Filtrage pour plus d'un critère"""
        InstructionRoleFactory(user=authenticate.user)
        # Rien ne devrait être trouvé car declaration5 a mint >= 10mg mais vitamin_c is 80mg (pas entre 90-100)
        dose = f"dose=plant||Mint||{self.mint.id}||≥||10||{self.unit_mg.id}&dose=substance||Vitamin C||{self.vitamin_c.id}||≬||90|100||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 0)

    @authenticate
    def test_invalid_dose_format(self):
        """Un filtre invalide ne retourne pas de résultats"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request("dose=invalid_format")
        self.assertEqual(len(results), 0)

    @authenticate
    def test_nonexistent_element(self):
        """Utiliser des IDs pour des objets non existants ne retourne pas de résultats"""
        InstructionRoleFactory(user=authenticate.user)
        results = self.make_request(f"dose=plant||Nonexistent||999||≥||10||{self.unit_mg.id}")
        self.assertEqual(len(results), 0)

    @authenticate
    def test_filter_plant_dose_with_gram_conversion(self):
        """Filtre utilisant l'unité "g" mais retournant une déclaration en "mg" """
        InstructionRoleFactory(user=authenticate.user)
        # La Declaration1 a 5mg camomille - on filtre > 0.004g (çad 4mg)
        dose = f"dose=plant||Camomille||{self.camomille.id}|{self.branch.id}|Branch||>||0.004||{self.unit_g.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration1.id)

    @authenticate
    def test_filter_substance_dose_with_milligram_conversion(self):
        """Filter utilisant des "mg" qui retourne une déclaration en "g" """
        InstructionRoleFactory(user=authenticate.user)
        # La Declaration4 a 0.5g de green tea - on filtre >= 400mg (çad 0.4g)
        dose = f"dose=ingredient||Green Tea Extract||{self.green_tea.id}||≥||400||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration4.id)

    @authenticate
    def test_filter_between_units(self):
        """La conversion de dose doit aussi marcher pour le filtre BETWEEN"""
        InstructionRoleFactory(user=authenticate.user)
        # Declaration2 a 12.5mg de caféine - on filtre entre 0.01g (10mg) et 0.02g (20mg)
        dose = f"dose=substance||Caffeine||{self.caffeine.id}||≬||0.01|0.02||{self.unit_g.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.declaration2.id)

    @authenticate
    def test_filter_with_non_convertible_units(self):
        """Si les unités ne peuvent pas être converties, le filtre marche quand même"""
        InstructionRoleFactory(user=authenticate.user)
        # Cette unité n'est pas supportée pour la conversion
        unit_iu = UnitFactory(name="IU", long_name="International Units")

        # Il y a un fallback a un filtrage sans conversion
        dose = f"dose=ingredient||Ginger Root||{self.ginger.id}||≥||5||{unit_iu.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 0)

    @authenticate
    def test_form_of_supply(self):
        InstructionRoleFactory(user=authenticate.user)
        vitamin_b12 = SubstanceFactory(name="Vitamin B12")
        cyanocobalamine = IngredientFactory(
            name="Cyanocobalamine",
            ingredient_type=IngredientType.FORM_OF_SUPPLY,
            substances=[vitamin_b12],
        )

        declaration = AuthorizedDeclarationFactory()
        DeclaredIngredientFactory(declaration=declaration, ingredient=cyanocobalamine)
        ComputedSubstanceFactory(declaration=declaration, substance=vitamin_b12, quantity=80.0, unit=self.unit_mg)

        other_declaration = AuthorizedDeclarationFactory()
        ComputedSubstanceFactory(
            declaration=other_declaration, substance=vitamin_b12, quantity=80.0, unit=self.unit_mg
        )

        # La recherche par forme d'apport doit chercher la dose de la substance qu'elle contient
        # via les computed substances. Seulement les déclarations contenant la forme d'apport doivent
        # être prises.

        dose = f"dose=form_of_supply||Cyanocobalamine||{cyanocobalamine.id}||≥||80||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)

    @authenticate
    def test_form_of_supply_without_substances(self):
        """
        Si une forme d'apport ou ingrédient actif n'a pas de substances liées le filtre
        par dose doit chercher par la quantité et unité spécifiée au niveau de l'ingrédient.
        Pour plus de détails regarder la fonction `showFields` de src/components/ElementCard.vue
        """
        InstructionRoleFactory(user=authenticate.user)
        sulfur = IngredientFactory(
            name="Soufre",
            ingredient_type=IngredientType.FORM_OF_SUPPLY,
            substances=[],
        )

        declaration = AuthorizedDeclarationFactory()
        DeclaredIngredientFactory(declaration=declaration, ingredient=sulfur, quantity=80.0, unit=self.unit_mg)

        dose = f"dose=form_of_supply||Soufre||{sulfur.id}||≥||80||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)

    @authenticate
    def test_active_ingredient(self):
        InstructionRoleFactory(user=authenticate.user)
        creatine = SubstanceFactory(name="Créatine")
        pyruvate_de_creatine = IngredientFactory(
            name="Pyruvate de créatine",
            ingredient_type=IngredientType.ACTIVE_INGREDIENT,
            substances=[creatine],
        )

        declaration = AuthorizedDeclarationFactory()
        DeclaredIngredientFactory(declaration=declaration, ingredient=pyruvate_de_creatine)
        ComputedSubstanceFactory(declaration=declaration, substance=creatine, quantity=80.0, unit=self.unit_mg)

        other_declaration = AuthorizedDeclarationFactory()
        ComputedSubstanceFactory(declaration=other_declaration, substance=creatine, quantity=80.0, unit=self.unit_mg)

        # La recherche par ingrédient actif doit chercher la dose de la substance qu'elle contient
        # via les computed substances. Seulement les déclarations contenant la forme d'apport doivent
        # être prises.

        dose = f"dose=active_ingredient||Pyruvate de créatine||{pyruvate_de_creatine.id}||≥||80||{self.unit_mg.id}"
        results = self.make_request(dose)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)

    @authenticate
    def test_multiple_dses(self):
        """Filtrage par plus d'une dose"""

        InstructionRoleFactory(user=authenticate.user)
        dose_1 = f"dose=plant||Camomille||{self.camomille.id}|{self.branch.id}|Branch||>||4||{self.unit_mg.id}"
        dose_2 = f"dose=substance||Caffeine||{self.caffeine.id}||≬||10|15||{self.unit_mg.id}"

        declaration = AuthorizedDeclarationFactory()
        DeclaredPlantFactory(
            declaration=declaration, plant=self.camomille, used_part=self.branch, quantity=5.0, unit=self.unit_mg
        )
        ComputedSubstanceFactory(declaration=declaration, substance=self.caffeine, quantity=12.5, unit=self.unit_mg)

        url = f"{reverse('api:list_all_declarations')}?{dose_1}&{dose_2}"
        response = self.client.get(url, format="json")
        results = response.json()["results"]

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], declaration.id)
