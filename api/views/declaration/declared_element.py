from rest_framework.exceptions import ParseError
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


class DeclaredElementView(RetrieveUpdateAPIView):
    permission_classes = [(IsInstructor | IsVisor)]

    type_mapping = {
        "plant": {
            "model": DeclaredPlant,
            "serializer": DeclaredPlantSerializer,
        },
        "microorganism": {
            "model": DeclaredMicroorganism,
            "serializer": DeclaredMicroorganismSerializer,
        },
        "substance": {
            "model": DeclaredSubstance,
            "serializer": DeclaredSubstanceSerializer,
        },
        "ingredient": {
            "model": DeclaredIngredient,
            "serializer": DeclaredIngredientSerializer,
        },
    }

    def get_queryset(self):
        return self.type_info["model"].objects.all()

    def get_serializer_class(self):
        return self.type_info["serializer"]

    @property
    def type_info(self):
        element_type = self.kwargs["type"]

        if element_type not in self.type_mapping:
            valid_type_list = list(self.type_mapping.keys())
            raise ParseError(detail=f"Unknown type: '{element_type}' not in {valid_type_list}")

        return self.type_mapping[element_type]
