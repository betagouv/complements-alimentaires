from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from data.models import DeclaredPlant, DeclaredSubstance, DeclaredIngredient, DeclaredMicroorganism, Declaration
from api.serializers import DeclaredElementSerializer, DeclaredPlantSerializer
from itertools import chain


class DeclaredElementsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class DeclaredElementsView(ListAPIView):
    serializer_class = DeclaredElementSerializer
    pagination_class = DeclaredElementsPagination

    def get_queryset(self):
        closed_statuses = [
            Declaration.DeclarationStatus.DRAFT,
            Declaration.DeclarationStatus.ABANDONED,
            Declaration.DeclarationStatus.REJECTED,
            Declaration.DeclarationStatus.WITHDRAWN,
        ]
        return list(
            chain(
                DeclaredPlant.objects.filter(new=True).exclude(declaration__status__in=closed_statuses),
                DeclaredSubstance.objects.filter(new=True).exclude(declaration__status__in=closed_statuses),
                DeclaredIngredient.objects.filter(new=True).exclude(declaration__status__in=closed_statuses),
                DeclaredMicroorganism.objects.filter(new=True).exclude(declaration__status__in=closed_statuses),
            )
        )


class DeclaredPlantView(RetrieveAPIView):
    serializer_class = DeclaredPlantSerializer
    queryset = DeclaredPlant.objects.all()
