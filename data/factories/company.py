import factory
from data.models.company import Company
from data.utils.string_utils import make_random_str
import string


def _make_siret() -> str:
    return make_random_str(size=14, chars=string.digits)


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    social_name = factory.Faker("company")
    commercial_name = factory.Faker("company")
    siret = factory.LazyFunction(_make_siret)
