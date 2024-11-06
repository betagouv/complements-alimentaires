from rest_framework.generics import ListAPIView
from data.models import DeclaredPlant, DeclaredSubstance, DeclaredIngredient, DeclaredMicroorganism
from api.serializers import DeclaredElementSerializer
from itertools import chain


class DeclaredIngredientsView(ListAPIView):
    serializer_class = DeclaredElementSerializer

    def get_queryset(self):
        return list(
            chain(
                DeclaredPlant.objects.all(),
                DeclaredSubstance.objects.all(),
                DeclaredIngredient.objects.all(),
                DeclaredMicroorganism.objects.all(),
            )
        )
