import random
import factory
from data.models import Microorganism, MicroorganismSynonym
from data.factories import SubstanceFactory


class MicroorganismFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Microorganism

    name = factory.Faker("text", max_nb_chars=20)
    name_en = factory.Faker("text", max_nb_chars=20)
    genre = factory.Faker("text", max_nb_chars=20)

    @factory.post_generation
    def substance(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.substance.add(SubstanceFactory.create())
        elif extracted:
            for substance in extracted:
                self.substance.add(substance)


class MicroorganismSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MicroorganismSynonym

    microorganism = factory.SubFactory(MicroorganismFactory)
    name = factory.Faker("text", max_nb_chars=20)
