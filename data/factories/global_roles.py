import factory

from data.models import ControlRole, InstructionRole, VisaRole

from .user import UserFactory


class InstructionRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InstructionRole

    user = factory.SubFactory(UserFactory)


class VisaRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VisaRole

    user = factory.SubFactory(UserFactory)


class ControlRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ControlRole

    user = factory.SubFactory(UserFactory)
