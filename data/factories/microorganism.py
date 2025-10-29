import random

import factory

from data.factories.substance import SubstanceFactory
from data.models import Microorganism, MicroorganismSynonym
from data.models.ingredient_status import IngredientStatus


class MicroorganismFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Microorganism
        django_get_or_create = ("siccrf_id",)

    siccrf_id = factory.Sequence(lambda n: n + 1)
    genus = factory.Faker("text", max_nb_chars=20)
    species = factory.Faker("text", max_nb_chars=20)
    status = IngredientStatus.AUTHORIZED
    to_be_entered_in_next_decree = False
    is_obsolete = False
    must_specify_quantity = False

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
