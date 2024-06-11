import factory

from data.models import Declaration, DeclaredPlant

from .company import CompanyFactory, DeclarantRoleFactory
from .condition import ConditionFactory
from .effect import EffectFactory
from .galenic_formulation import GalenicFormulationFactory
from .global_roles import InstructionRoleFactory
from .plant import PlantFactory
from .population import PopulationFactory
from .unit import SubstanceUnitFactory


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


class InstructionReadyDeclarationFactory(CompleteDeclarationFactory):
    pass


class InstructionOngoingDeclarationFactory(CompleteDeclarationFactory):
    status = Declaration.DeclarationStatus.ONGOING_INSTRUCTION
    author = factory.SubFactory(DeclarantRoleFactory)
    instructor = factory.SubFactory(InstructionRoleFactory)
