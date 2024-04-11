import factory
from data.models.company import Company
from data.utils.string_utils import make_random_str
from data.choices import CountryChoices
import string
import random


def _make_siret() -> str:
    return make_random_str(size=14, chars=string.digits)


def _make_vat() -> str:
    return random.choice(CountryChoices.values) + make_random_str(size=12, chars=string.digits)


def _make_country_code() -> str:
    return random.choice(list(CountryChoices))


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    social_name = factory.Faker("company")
    commercial_name = factory.Faker("company")
    siret = factory.LazyFunction(_make_siret)
    address = factory.Faker("street_address")
    postal_code = factory.Faker("postcode")
    city = factory.Faker("city")
    country = factory.LazyFunction(_make_country_code)


class CompanyWithSiretFactory(CompanyFactory):
    pass


class CompanyWithVatFactory(CompanyFactory):
    vat = factory.LazyFunction(_make_vat)
