import factory
from factory.fuzzy import FuzzyText
from data.models import SubstanceUnit


class SubstanceUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubstanceUnit
        django_get_or_create = ("siccrf_id",)

    siccrf_id = factory.Sequence(lambda n: n + 1)
    name = FuzzyText(length=2)
    long_name = factory.Faker("text", max_nb_chars=20)
