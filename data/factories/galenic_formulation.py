import factory
from data.models import GalenicFormulation


class GalenicFormulationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GalenicFormulation

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    ca_name = factory.Faker("text", max_nb_chars=20)
    siccrf_name_en = factory.Faker("text", max_nb_chars=20)
