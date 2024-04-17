import factory
from data.models import IngredientStatus


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IngredientStatus
        django_get_or_create = ("siccrf_id",)

    name = (factory.fuzzy.FuzzyChoice(["Autorisé", "Non autorisé", "A inscrire", "Sans objet"]),)
    siccrf_id = factory.Sequence(lambda n: n + 1)
