import random

import factory

from data.factories.substance import SubstanceFactory
from data.models import Ingredient, IngredientSynonym, IngredientType
from data.models.ingredient_status import IngredientStatus


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=15)
    siccrf_name_en = factory.Faker("text", max_nb_chars=15)
    siccrf_id = factory.Sequence(lambda n: n + 1)
    description = factory.Faker("text", max_nb_chars=160)
    status = IngredientStatus.AUTHORIZED
    to_be_entered_in_next_decree = False
    ingredient_type = IngredientType.ACTIVE_INGREDIENT
    is_obsolete = False

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


class IngredientSynonymFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IngredientSynonym

    standard_name = factory.SubFactory(IngredientFactory)
    name = factory.Faker("text", max_nb_chars=20)
