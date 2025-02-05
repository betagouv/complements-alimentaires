import abc
from django.db import transaction
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
    PlantSynonym,
    MicroorganismSynonym,
    SubstanceSynonym,
    IngredientSynonym,
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


TYPE_MAPPING = {
    "plant": {
        "model": DeclaredPlant,
        "synonym_model": PlantSynonym,
        "serializer": DeclaredPlantSerializer,
    },
    "microorganism": {
        "model": DeclaredMicroorganism,
        "synonym_model": MicroorganismSynonym,
        "serializer": DeclaredMicroorganismSerializer,
    },
    "substance": {
        "model": DeclaredSubstance,
        "synonym_model": SubstanceSynonym,
        "serializer": DeclaredSubstanceSerializer,
    },
    "other-ingredient": {
        "model": DeclaredIngredient,
        "synonym_model": IngredientSynonym,
        "serializer": DeclaredIngredientSerializer,
        "attribute": "ingredient",
    },
}


class ElementMappingMixin:
    @property
    def element_type(self):
        return self.kwargs["type"]

    @property
    def type_info(self):
        if self.element_type not in TYPE_MAPPING:
            valid_type_list = list(TYPE_MAPPING.keys())
            raise ParseError(detail=f"Unknown type: '{self.element_type}' not in {valid_type_list}")

        return TYPE_MAPPING[self.element_type]

    @property
    def type_model(self):
        return self.type_info["model"]

    @property
    def type_serializer(self):
        return self.type_info["serializer"]

    @property
    def synonym_model(self):
        return self.type_info["synonym_model"]


class DeclaredElementView(RetrieveAPIView, ElementMappingMixin):
    permission_classes = [(IsInstructor | IsVisor)]

    def get_queryset(self):
        return self.type_model.objects.all()

    def get_serializer_class(self):
        return self.type_serializer


class DeclaredElementActionAbstractView(APIView, ElementMappingMixin):
    permission_classes = [(IsInstructor | IsVisor)]
    __metaclass__ = abc.ABCMeta

    @transaction.atomic
    def post(self, request, pk, type):
        element = get_object_or_404(self.type_model, pk=pk)

        element_to_save = self._update_element(element, request)
        element_to_save.save()

        return Response(self.type_serializer(element_to_save, context={"request": request}).data)

    @abc.abstractmethod
    def _update_element(self, element, request):
        pass


class DeclaredElementRequestInfoView(DeclaredElementActionAbstractView):
    def _update_element(self, element, request):
        element.request_status = self.type_model.AddableStatus.INFORMATION
        element.request_private_notes = request.data.get("request_private_notes")
        return element


class DeclaredElementRejectView(DeclaredElementActionAbstractView):
    def _update_element(self, element, request):
        element.request_status = self.type_model.AddableStatus.REJECTED
        element.request_private_notes = request.data.get("request_private_notes")
        return element


class DeclaredElementReplaceView(DeclaredElementActionAbstractView):
    def _update_element(self, declared_element, request):
        try:
            replacement_element_id = request.data["element"]["id"]
            replacement_type = request.data["element"]["type"]
        except KeyError:
            raise ParseError(detail="Must provide a dict 'element' with id and type")

        # utiliser les valeurs serialisées pour MAJ ou créer l'element déclaré
        element_data = self.type_serializer(declared_element).data
        additional_fields = request.data.get("additional_fields", {})
        element_data.update(additional_fields)
        element_data.update(
            {
                "element": {"id": replacement_element_id},
                "request_status": self.type_model.AddableStatus.REPLACED,
                "new": False,
            }
        )

        new_type = TYPE_MAPPING[replacement_type]
        if replacement_type != self.element_type:
            # gérer le difference en nom entre microorganismes et les autres types
            if replacement_type == "microorganism":
                element_data["new_species"] = declared_element.new_name
            elif self.element_type == "microorganism":
                element_data["new_name"] = declared_element.new_name

            serializer = new_type["serializer"](data=element_data)
            serializer.is_valid(raise_exception=True)

            serializer.validated_data["declaration"] = declared_element.declaration

            new_declared_element = serializer.create(serializer.validated_data)
            declared_element.delete()
            declared_element = new_declared_element
        else:
            serializer = self.type_serializer(declared_element, data=element_data, partial=True)
            serializer.is_valid(raise_exception=True)
            declared_element = serializer.save()

        replacement_synonym_model = new_type["synonym_model"]
        synonyms = request.data.get("synonyms", [])
        replacement_type_attribute = new_type.get("attribute", replacement_type)
        replacement_element = getattr(declared_element, replacement_type_attribute)
        # TODO: refactor to share logic with create/update ingredient endpoints?
        for synonym in synonyms:
            try:
                name = synonym["name"]
                if name and not replacement_synonym_model.objects.filter(name=name).exists():
                    replacement_synonym_model.objects.create(standard_name=replacement_element, name=name)
            except KeyError:
                raise ParseError(detail="Must provide 'name' to create new synonym")

        return declared_element
