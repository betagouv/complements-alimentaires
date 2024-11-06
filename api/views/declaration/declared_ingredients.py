from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from data.models import DeclaredPlant, DeclaredSubstance, DeclaredIngredient, DeclaredMicroorganism
from api.serializers import DeclaredElementSerializer
from itertools import chain


class DeclaredElementsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class DeclaredElementsView(ListAPIView):
    serializer_class = DeclaredElementSerializer
    pagination_class = DeclaredElementsPagination

    def get_queryset(self):
        return list(
            chain(
                DeclaredPlant.objects.filter(new=True),
                DeclaredSubstance.objects.filter(new=True),
                DeclaredIngredient.objects.filter(new=True),
                DeclaredMicroorganism.objects.filter(new=True),
            )
        )
