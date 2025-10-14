import factory

from data.models import Unit


class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unit
        django_get_or_create = ("siccrf_id",)

    siccrf_id = factory.Sequence(lambda n: n + 1)

    # Génere des séquences uniques (aaa, aab, aac) pour éviter des problèmes avec le unique=True
    name = factory.Sequence(
        lambda n: "{}{}{}".format(
            chr(97 + (n // (26 * 26)) % 26),
            chr(97 + (n // 26) % 26),
            chr(97 + n % 26),
        ).lower()
    )
    long_name = factory.Faker("text", max_nb_chars=20)
