import factory
from data.models import Condition


class ConditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Condition

    name = factory.Faker("text", max_nb_chars=20)
    name_en = factory.Faker("text", max_nb_chars=20)
