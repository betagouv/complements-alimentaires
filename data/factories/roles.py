import factory

from data.models.roles import BaseRole, CompanySupervisor, Declarant

from .company import CompanyFactory
from .user import UserFactory


class BaseRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseRole
        abstract = True

    user = factory.SubFactory(UserFactory)


class DeclarantFactory(BaseRoleFactory):
    class Meta:
        model = Declarant

    @factory.post_generation
    def companies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for company in extracted:
                self.companies.add(company)
        else:
            for _ in range(3):
                self.companies.add(CompanyFactory())


class CompanySupervisorFactory(BaseRoleFactory):
    class Meta:
        model = CompanySupervisor

    @factory.post_generation
    def companies(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.companies.add(*extracted)
