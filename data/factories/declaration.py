import factory

from data.models import Declaration, DeclaredIngredient, DeclaredMicroorganism, DeclaredPlant, DeclaredSubstance

from .company import CompanyFactory
from .condition import ConditionFactory
from .effect import EffectFactory
from .galenic_formulation import GalenicFormulationFactory
from .global_roles import InstructionRoleFactory
from .ingredient import IngredientFactory
from .microorganism import MicroorganismFactory
from .plant import PlantFactory
from .population import PopulationFactory
from .substance import SubstanceFactory
from .unit import SubstanceUnitFactory
from .user import UserFactory


class DeclarationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Declaration

    company = factory.SubFactory(CompanyFactory)
    status = Declaration.DeclarationStatus.DRAFT
    name = factory.Faker("text", max_nb_chars=20)
    brand = factory.Faker("company")
    gamme = factory.Faker("bs")
    flavor = factory.Faker("text", max_nb_chars=20)
    description = factory.Faker("text", max_nb_chars=20)


class DeclaredPlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeclaredPlant

    plant = factory.SubFactory(PlantFactory)
    quantity = factory.Faker("pyfloat")
    unit = factory.SubFactory(SubstanceUnitFactory)


class DeclaredMicroorganismFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeclaredMicroorganism

    microorganism = factory.SubFactory(MicroorganismFactory)
    active = factory.Faker("boolean")
    quantity = factory.Faker("pyfloat")


class DeclaredIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeclaredIngredient

    ingredient = factory.SubFactory(IngredientFactory)
    active = factory.Faker("boolean")


class DeclaredSubstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeclaredSubstance

    substance = factory.SubFactory(SubstanceFactory)
    active = factory.Faker("boolean")


class CompleteDeclarationFactory(DeclarationFactory):
    class Meta:
        model = Declaration

    daily_recommended_dose = factory.Faker("text", max_nb_chars=20)
    minimum_duration = factory.Faker("text", max_nb_chars=20)
    unit_quantity = factory.Faker("pyfloat")
    unit_measurement = factory.SubFactory(SubstanceUnitFactory)
    galenic_formulation = factory.SubFactory(GalenicFormulationFactory)
    address = factory.Faker("street_address", locale="FR")
    postal_code = factory.Faker("postcode", locale="FR")
    city = factory.Faker("city", locale="FR")
    country = "FR"

    @factory.post_generation
    def conditions_not_recommended(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for condition in extracted:
                self.conditions_not_recommended.add(condition)
        else:
            for _ in range(3):
                self.conditions_not_recommended.add(ConditionFactory())

    @factory.post_generation
    def populations(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for population in extracted:
                self.populations.add(population)
        else:
            for _ in range(3):
                self.populations.add(PopulationFactory())

    @factory.post_generation
    def effects(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for effect in extracted:
                self.effects.add(effect)
        else:
            for _ in range(3):
                self.effects.add(EffectFactory())

    @factory.post_generation
    def declared_plants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for declared_plant in extracted:
                self.declared_plants.add(declared_plant)
        else:
            for _ in range(3):
                self.declared_plants.add(DeclaredPlantFactory(declaration=self))

    @factory.post_generation
    def declared_microorganisms(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for declared_microorganism in extracted:
                self.declared_microorganisms.add(declared_microorganism)
        else:
            for _ in range(3):
                self.declared_microorganisms.add(DeclaredMicroorganismFactory(declaration=self))

    @factory.post_generation
    def declared_ingredients(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for declared_ingredient in extracted:
                self.declared_ingredients.add(declared_ingredient)
        else:
            for _ in range(3):
                self.declared_ingredients.add(DeclaredIngredientFactory(declaration=self))

    @factory.post_generation
    def declared_substances(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for declared_substance in extracted:
                self.declared_substances.add(declared_substance)
        else:
            for _ in range(3):
                self.declared_substances.add(DeclaredSubstanceFactory(declaration=self))


class InstructionReadyDeclarationFactory(CompleteDeclarationFactory):
    author = factory.SubFactory(UserFactory)


class AwaitingInstructionDeclarationFactory(CompleteDeclarationFactory):
    status = Declaration.DeclarationStatus.AWAITING_INSTRUCTION
    author = factory.SubFactory(UserFactory)


class OngoingInstructionDeclarationFactory(CompleteDeclarationFactory):
    status = Declaration.DeclarationStatus.ONGOING_INSTRUCTION
    author = factory.SubFactory(UserFactory)
    instructor = factory.SubFactory(InstructionRoleFactory)


class ObservationDeclarationFactory(CompleteDeclarationFactory):
    status = Declaration.DeclarationStatus.OBSERVATION
    author = factory.SubFactory(UserFactory)
    instructor = factory.SubFactory(InstructionRoleFactory)
