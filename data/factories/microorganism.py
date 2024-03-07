import random
import factory
from data.models import Microorganism, MicroorganismSynonym
from data.factories import SubstanceFactory


class MicroorganismFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Microorganism
        django_get_or_create = ("siccrf_id",)

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    ca_name = factory.Faker("text", max_nb_chars=20)
    siccrf_name_en = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Faker("random_int", min=1, max=2000)
    siccrf_genre = factory.Faker("text", max_nb_chars=20)
    ca_genre = factory.Faker("text", max_nb_chars=20)

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
