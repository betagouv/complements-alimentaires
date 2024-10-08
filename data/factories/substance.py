import factory

from data.factories.unit import SubstanceUnitFactory
from data.models import Substance, SubstanceSynonym
from data.models.ingredient_status import IngredientStatus


class SubstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Substance
        django_get_or_create = ("siccrf_id",)

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    ca_name = factory.Faker("text", max_nb_chars=20)
    siccrf_name_en = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    siccrf_must_specify_quantity = factory.Faker("boolean")
    siccrf_max_quantity = factory.Faker("random_int", min=0, max=20)
    siccrf_nutritional_reference = factory.Faker("random_int", min=0, max=20)
    ca_must_specify_quantity = factory.Faker("boolean")
    ca_max_quantity = factory.Faker("random_int", min=0, max=20)
    ca_nutritional_reference = factory.Faker("random_int", min=0, max=20)
    unit = factory.SubFactory(SubstanceUnitFactory)
    siccrf_status = IngredientStatus.AUTHORIZED
    to_be_entered_in_next_decree = False
    siccrf_is_obsolete = False
    ca_is_obsolete = False


class SubstanceSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubstanceSynonym

    standard_name = factory.SubFactory(SubstanceFactory)
    name = factory.Faker("text", max_nb_chars=20)
