import random
import factory
from data.models import Microorganism, MicroorganismSynonym
from data.factories.substance import SubstanceFactory
from data.factories.status import StatusFactory


class MicroorganismFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Microorganism
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    siccrf_genus = factory.Faker("text", max_nb_chars=20)
    ca_genus = factory.Faker("text", max_nb_chars=20)
    siccrf_species = factory.Faker("text", max_nb_chars=20)
    ca_species = factory.Faker("text", max_nb_chars=20)
    status = factory.SubFactory(StatusFactory, name="Autorisé")

    @factory.post_generation
    def substances(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.substances.add(SubstanceFactory.create())
        elif extracted:
            for substance in extracted:
                self.substances.add(substance)


class MicroorganismSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MicroorganismSynonym

    standard_name = factory.SubFactory(MicroorganismFactory)
    name = factory.Faker("text", max_nb_chars=20)
