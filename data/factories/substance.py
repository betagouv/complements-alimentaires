import factory

from data.factories.population import PopulationFactory
from data.factories.unit import SubstanceUnitFactory
from data.models.ingredient_status import IngredientStatus
from data.models.substance import Substance, SubstanceMaxQuantityPerPopulationRelation, SubstanceSynonym


class SubstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Substance
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    must_specify_quantity = factory.Faker("boolean")
    nutritional_reference = factory.Faker("random_int", min=0, max=20)
    unit = factory.SubFactory(SubstanceUnitFactory)
    status = IngredientStatus.AUTHORIZED
    to_be_entered_in_next_decree = False
    is_obsolete = False


class SubstanceMaxQuantityPerPopulationRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubstanceMaxQuantityPerPopulationRelation

    population = factory.SubFactory(PopulationFactory)
    substance = factory.SubFactory(SubstanceFactory)
    max_quantity = factory.Faker("random_int", min=0, max=20)


class SubstanceSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubstanceSynonym

    standard_name = factory.SubFactory(SubstanceFactory)
    name = factory.Faker("text", max_nb_chars=20)
