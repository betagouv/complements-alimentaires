from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from data.models import DeclaredPlant, DeclaredSubstance, DeclaredIngredient, DeclaredMicroorganism, Declaration
from api.serializers import (
    DeclaredElementSerializer,
    DeclaredPlantSerializer,
    DeclaredMicroorganismSerializer,
    DeclaredSubstanceSerializer,
    DeclaredIngredientSerializer,
)
from api.permissions import IsInstructor, IsVisor
from itertools import chain


class DeclaredElementsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class DeclaredElementsView(ListAPIView):
    serializer_class = DeclaredElementSerializer
    pagination_class = DeclaredElementsPagination
    permission_classes = [(IsInstructor | IsVisor)]

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


class DeclaredPlantView(RetrieveUpdateAPIView):
    permission_classes = [(IsInstructor | IsVisor)]
    serializer_class = DeclaredPlantSerializer
    queryset = DeclaredPlant.objects.all()


class DeclaredMicroorganismView(RetrieveUpdateAPIView):
    permission_classes = [(IsInstructor | IsVisor)]
    serializer_class = DeclaredMicroorganismSerializer
    queryset = DeclaredMicroorganism.objects.all()


class DeclaredSubstanceView(RetrieveUpdateAPIView):
    permission_classes = [(IsInstructor | IsVisor)]
    serializer_class = DeclaredSubstanceSerializer
    queryset = DeclaredSubstance.objects.all()


class DeclaredIngredientView(RetrieveUpdateAPIView):
    permission_classes = [(IsInstructor | IsVisor)]
    serializer_class = DeclaredIngredientSerializer
    queryset = DeclaredIngredient.objects.all()
