import factory
from factory.fuzzy import FuzzyText
from data.models import SubstanceUnit


class SubstanceUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubstanceUnit

    siccrf_id = factory.Faker("random_int", min=1)
    name = FuzzyText(length=2)
    long_name = factory.Faker("text", max_nb_chars=20)
