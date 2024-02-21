import factory
from data.models import Condition


class ConditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Condition

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    CA_name = factory.Faker("text", max_nb_chars=20)
    siccrf_name_en = factory.Faker("text", max_nb_chars=20)
