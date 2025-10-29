import random

import factory

from data.factories.substance import SubstanceFactory
from data.models import Plant, PlantFamily, PlantPart, PlantSynonym
from data.models.ingredient_status import IngredientStatus


class PlantPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantPart
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=10)
    siccrf_name_en = factory.Faker("text", max_nb_chars=10)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    is_obsolete = False
    must_specify_quantity = False


class PlantFamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantFamily
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=25)
    siccrf_name_en = factory.Faker("text", max_nb_chars=25)
    siccrf_id = factory.Sequence(lambda n: n + 1)


class PlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plant
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    family = factory.SubFactory(PlantFamilyFactory)
    status = IngredientStatus.AUTHORIZED
    to_be_entered_in_next_decree = False

    @factory.post_generation
    def substances(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted or isinstance(extracted, list):
            for substance in extracted:
                self.substances.add(substance)
        else:
            for _ in range(random.randint(1, 4)):
                self.substances.add(SubstanceFactory.create())

    @factory.post_generation
    def plant_parts(self, create, extracted, **kwargs):
        if create:
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
