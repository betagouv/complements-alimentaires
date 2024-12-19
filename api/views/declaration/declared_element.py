import abc
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from data.models import (
    DeclaredPlant,
    DeclaredSubstance,
    DeclaredIngredient,
    DeclaredMicroorganism,
    Declaration,
    Plant,
    Microorganism,
    Substance,
    Ingredient,
)
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


class ElementMappingMixin:
    type_mapping = {
        "plant": {
            "model": DeclaredPlant,
            "element_model": Plant,
            "serializer": DeclaredPlantSerializer,
        },
        "microorganism": {
            "model": DeclaredMicroorganism,
            "element_model": Microorganism,
            "serializer": DeclaredMicroorganismSerializer,
        },
        "substance": {
            "model": DeclaredSubstance,
            "element_model": Substance,
            "serializer": DeclaredSubstanceSerializer,
        },
        "ingredient": {
            "model": DeclaredIngredient,
            "element_model": Ingredient,
            "serializer": DeclaredIngredientSerializer,
        },
    }

    @property
    def element_type(self):
        return self.kwargs["type"]

    @property
    def type_info(self):
        if self.element_type not in self.type_mapping:
            valid_type_list = list(self.type_mapping.keys())
            raise ParseError(detail=f"Unknown type: '{self.element_type}' not in {valid_type_list}")

        return self.type_mapping[self.element_type]

    @property
    def type_model(self):
        return self.type_info["model"]

    @property
    def type_serializer(self):
        return self.type_info["serializer"]

    @property
    def element_model(self):
        return self.type_info["element_model"]


class DeclaredElementView(RetrieveAPIView, ElementMappingMixin):
    permission_classes = [(IsInstructor | IsVisor)]

    def get_queryset(self):
        return self.type_model.objects.all()

    def get_serializer_class(self):
        return self.type_serializer


class DeclaredElementActionAbstractView(APIView, ElementMappingMixin):
    permission_classes = [(IsInstructor | IsVisor)]
    __metaclass__ = abc.ABCMeta

    def post(self, request, pk, type):
        element = get_object_or_404(self.type_model, pk=pk)

        self._update_element(element, request)
        element.save()

        return Response(self.type_serializer(element).data)

    @abc.abstractmethod
    def _update_element(self, element, request):
        pass


class DeclaredElementRequestInfoView(DeclaredElementActionAbstractView):
    def _update_element(self, element, request):
        element.request_status = self.type_model.AddableStatus.INFORMATION
        element.request_private_notes = request.data.get("request_private_notes")


class DeclaredElementRejectView(DeclaredElementActionAbstractView):
    def _update_element(self, element, request):
        element.request_status = self.type_model.AddableStatus.REJECTED
        element.request_private_notes = request.data.get("request_private_notes")


class DeclaredElementReplaceView(DeclaredElementActionAbstractView):
    def _update_element(self, element, request):
        try:
            existing_element_id = request.data["element"]["id"]
            # existing_element_type = request.data["element"]["type"]
        except KeyError:
            raise ParseError(detail="Must provide a dict 'element' with id and type")

        try:
            existing_element = self.element_model.objects.get(pk=existing_element_id)
        except self.element_model.DoesNotExist:
            raise ParseError(detail=f"No {self.element_type} exists with id {existing_element_id}")

        setattr(element, self.element_type, existing_element)
        element.request_status = self.type_model.AddableStatus.REPLACED
