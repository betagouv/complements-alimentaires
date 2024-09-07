import factory

from data.models import Preparation


class PreparationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Preparation

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    ca_name = factory.Faker("text", max_nb_chars=20)
