import random
import factory
from data.models import Plant, PlantSynonym, PlantPart, PlantFamily
from data.factories import SubstanceFactory


class PlantPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantPart
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=10)
    name_en = factory.Faker("text", max_nb_chars=10)
    siccrf_id = factory.Faker("random_int", min=1, max=20)


class PlantFamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantFamily
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=25)
    name_en = factory.Faker("text", max_nb_chars=25)
    siccrf_id = factory.Faker("random_int", min=1, max=20)


class PlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plant
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Faker("random_int", min=1, max=2000)
    family = factory.SubFactory(PlantFamilyFactory)

    @factory.post_generation
    def substances(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.substances.add(SubstanceFactory.create())
        elif extracted:
            for substance in extracted:
                self.substances.add(substance)

    @factory.post_generation
    def useful_parts(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.useful_parts.add(PlantPartFactory.create())
        elif extracted:
            for useful_part in extracted:
                self.useful_parts.add(useful_part)


class PlantSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantSynonym

    standard_name = factory.SubFactory(PlantFactory)
    name = factory.Faker("text", max_nb_chars=20)
