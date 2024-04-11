import factory
from data.models import Effect


class EffectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Effect

    siccrf_name = factory.Faker("text", max_nb_chars=20)
    ca_name = factory.Faker("text", max_nb_chars=20)
    siccrf_name_en = factory.Faker("text", max_nb_chars=20)
