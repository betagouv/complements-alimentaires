import random
import factory
from data.models import Plant, PlantSynonym, PlantPart, Family
from data.factories import SubstanceFactory


class PlantPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlantPart

    name = factory.Faker("text", max_nb_chars=10)
    name_en = factory.Faker("text", max_nb_chars=10)


class FamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Family

    name = factory.Faker("text", max_nb_chars=25)
    name_en = factory.Faker("text", max_nb_chars=25)


class PlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plant

    name = factory.Faker("text", max_nb_chars=20)
    name_en = factory.Faker("text", max_nb_chars=20)
    family = factory.SubFactory(FamilyFactory)

    @factory.post_generation
    def substance(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.substance.add(SubstanceFactory.create())
        elif extracted:
            for substance in extracted:
                self.substance.add(substance)

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

    plant = factory.SubFactory(PlantFactory)
    name = factory.Faker("text", max_nb_chars=20)
