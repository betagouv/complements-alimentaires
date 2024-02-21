import factory
from data.models import Population


class PopulationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Population

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    CA_name = factory.Faker("text", max_nb_chars=20)
