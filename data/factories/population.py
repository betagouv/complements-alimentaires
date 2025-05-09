import factory
from data.models import Population


class PopulationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Population

    name = factory.Faker("text", max_nb_chars=20)
