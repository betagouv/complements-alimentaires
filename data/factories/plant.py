import random

import factory

from data.factories.substance import SubstanceFactory
from data.models import Plant, PlantFamily, PlantPart, PlantSynonym
from data.models.ingredient_status import IngredientStatus


class PlantPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantPart
        django_get_or_create = ("siccrf_id",)

    siccrf_name = factory.Faker("text", max_nb_chars=10)
    ca_name = factory.Faker("text", max_nb_chars=10)
    siccrf_name_en = factory.Faker("text", max_nb_chars=10)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    siccrf_is_obsolete = False
    ca_is_obsolete = False


class PlantFamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantFamily
        django_get_or_create = ("siccrf_id",)

    siccrf_name = factory.Faker("text", max_nb_chars=25)
    ca_name = factory.Faker("text", max_nb_chars=25)
    siccrf_name_en = factory.Faker("text", max_nb_chars=25)
    siccrf_id = factory.Sequence(lambda n: n + 1)


class PlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plant
        django_get_or_create = ("siccrf_id",)

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    ca_name = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    siccrf_family = factory.SubFactory(PlantFamilyFactory)
    ca_family = factory.SubFactory(PlantFamilyFactory)
    siccrf_status = IngredientStatus.AUTHORIZED
    to_be_entered_in_next_decree = False

    @factory.post_generation
    def substances(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.substances.add(SubstanceFactory.create())
        elif extracted:
            for substance in extracted:
                self.substances.add(substance)

    @factory.post_generation
    def plant_parts(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.plant_parts.add(PlantPartFactory.create())
        elif extracted:
            for useful_part in extracted:
                self.plant_parts.add(useful_part)


class PlantSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantSynonym

    standard_name = factory.SubFactory(PlantFactory)
    name = factory.Faker("text", max_nb_chars=20)
