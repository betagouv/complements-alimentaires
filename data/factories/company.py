import random
import string

import factory
import faker
from phonenumber_field.phonenumber import PhoneNumber

from data.choices import CountryChoices
from data.models.company import ActivityChoices, Company, DeclarantRole, SupervisorRole
from data.utils.string_utils import make_random_str

from .user import UserFactory


def _make_siret() -> str:
    return faker.Faker("fr_FR").siret().replace(" ", "")


def _make_vat() -> str:
    return random.choice(CountryChoices.values) + make_random_str(size=12, chars=string.digits)


def _make_country_code() -> str:
    return random.choice(list(CountryChoices))


def _make_activities() -> list[str]:
    nb_activities = random.randint(1, len(list(ActivityChoices)))
    return random.sample(list(ActivityChoices), nb_activities)


def _make_phone_number():
    """On n'utilise pas Faker ou random ici car la lib PhoneNumber est très (trop ?) stricte sur la validation des numéros"""
    return PhoneNumber.from_string("06 10 20 30 40", region="FR")


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    social_name = factory.Faker("company", locale="FR")
    commercial_name = factory.Faker("company", locale="FR")
    siret = factory.LazyFunction(_make_siret)
    address = factory.Faker("street_address", locale="FR")
    postal_code = factory.Faker("postcode", locale="FR")
    city = factory.Faker("city", locale="FR")
    country = factory.LazyFunction(_make_country_code)
    activities = factory.LazyFunction(_make_activities)
    # contact
    phone_number = factory.LazyFunction(_make_phone_number)
    email = factory.Faker("email", locale="FR")


class CompanyWithSiretFactory(CompanyFactory):
    pass


class CompanyWithVatFactory(CompanyFactory):
    vat = factory.LazyFunction(_make_vat)


class SupervisorRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SupervisorRole

    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)


class DeclarantRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeclarantRole

    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
