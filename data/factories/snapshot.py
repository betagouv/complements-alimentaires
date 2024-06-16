import factory
import factory.fuzzy

from data.models import Declaration, Snapshot

from .declaration import DeclarationFactory
from .user import UserFactory


class SnapshotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Snapshot

    declaration = factory.SubFactory(DeclarationFactory)
    user = factory.SubFactory(UserFactory)
    status = factory.fuzzy.FuzzyChoice(Declaration.DeclarationStatus)
    comment = factory.Faker("text", max_nb_chars=40)
    json_declaration = {}
