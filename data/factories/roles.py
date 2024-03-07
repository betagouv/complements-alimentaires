import factory
from data.models.roles import BaseRole, Declarant, CompanySupervisor

from .user import UserFactory
from .company import CompanyFactory


class BaseRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseRole
        abstract = True

    user = factory.SubFactory(UserFactory)


class DeclarantFactory(BaseRoleFactory):
    class Meta:
        model = Declarant


class CompanySupervisorFactory(BaseRoleFactory):
    class Meta:
        model = CompanySupervisor

    company = factory.SubFactory(CompanyFactory)
