import random
import factory
from data.models import Ingredient, IngredientSynonym
from data.factories import SubstanceFactory


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient
        django_get_or_create = ("siccrf_id",)

    siccrf_name = factory.Faker("text", max_nb_chars=15)
    ca_name = factory.Faker("text", max_nb_chars=15)
    siccrf_name_en = factory.Faker("text", max_nb_chars=15)
    siccrf_id = factory.Faker("random_int", min=1, max=2000)
    siccrf_description = factory.Faker("text", max_nb_chars=160)

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

    standard_name = factory.SubFactory(IngredientFactory)
    name = factory.Faker("text", max_nb_chars=20)
