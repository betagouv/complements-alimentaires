import factory

from data.models.roles import BaseRole, CompanySupervisor, Declarant

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
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.companies.add(*extracted)


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
