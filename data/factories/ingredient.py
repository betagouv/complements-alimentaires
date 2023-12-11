import random
import factory
from data.models import Ingredient, IngredientSynonym
from data.factories import SubstanceFactory


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory.Faker("text", max_nb_chars=15)
    name_en = factory.Faker("text", max_nb_chars=15)
    description = factory.Faker("text", max_nb_chars=160)

    @factory.post_generation
    def substances(self, created, extracted, **kwargs):
        if created:
            for _ in range(random.randint(1, 4)):
                self.substances.add(SubstanceFactory.create())
        elif extracted:
            for substance in extracted:
                self.substances.add(substance)


class IngredientSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IngredientSynonym

    ingredient = factory.SubFactory(IngredientFactory)
    name = factory.Faker("text", max_nb_chars=20)
