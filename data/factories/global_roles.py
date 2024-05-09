import factory

from data.models import InstructionRole

from .user import UserFactory


class InstructionRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InstructionRole

    user = factory.SubFactory(UserFactory)
