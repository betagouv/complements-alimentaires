import factory
from data.models import Substance, SubstanceSynonym


class SubstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Substance
        django_get_or_create = ("siccrf_id",)

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    ca_name = factory.Faker("text", max_nb_chars=20)
    siccrf_name_en = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Faker("random_int", min=1, max=2000)
    siccrf_must_specify_quantity = factory.Faker("boolean")
    siccrf_max_quantity = factory.Faker("random_int", min=0, max=20)
    siccrf_nutritional_reference = factory.Faker("random_int", min=0, max=20)
    ca_must_specify_quantity = factory.Faker("boolean")
    ca_max_quantity = factory.Faker("random_int", min=0, max=20)
    ca_nutritional_reference = factory.Faker("random_int", min=0, max=20)


class SubstanceSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubstanceSynonym

    standard_name = factory.SubFactory(SubstanceFactory)
    name = factory.Faker("text", max_nb_chars=20)
