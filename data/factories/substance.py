import factory
from data.models import Substance


class SubstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Substance
        django_get_or_create = ("siccrf_id",)

    name = factory.Faker("text", max_nb_chars=20)
    name_en = factory.Faker("text", max_nb_chars=20)
    siccrf_id = factory.Faker("random_int", min=1, max=2000)
    must_specify_quantity = factory.Faker("boolean")
    min_quantity = factory.Faker("random_int", min=0, max=20)
    max_quantity = factory.Faker("random_int", min=0, max=20)
    nutritional_reference = factory.Faker("random_int", min=0, max=20)
