import factory
from .company import CompanyFactory
from data.models import Declaration


class DeclarationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Declaration

    company = factory.SubFactory(CompanyFactory)
    status = Declaration.DeclarationStatus.DRAFT
    name = factory.Faker("text", max_nb_chars=20)
    brand = factory.Faker("company")
    gamme = factory.Faker("bs")
    flavor = factory.Faker("text", max_nb_chars=20)
    description = factory.Faker("text", max_nb_chars=20)
