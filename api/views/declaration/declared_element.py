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
        "element_model": Plant,
        "synonym_model": PlantSynonym,
        "serializer": DeclaredPlantSerializer,
    },
    "microorganism": {
        "model": DeclaredMicroorganism,
        "element_model": Microorganism,
        "synonym_model": MicroorganismSynonym,
        "serializer": DeclaredMicroorganismSerializer,
    },
    "substance": {
        "model": DeclaredSubstance,
        "element_model": Substance,
        "synonym_model": SubstanceSynonym,
        "serializer": DeclaredSubstanceSerializer,
    },
    "other-ingredient": {
        "model": DeclaredIngredient,
        "element_model": Ingredient,
        "synonym_model": IngredientSynonym,
        "serializer": DeclaredIngredientSerializer,
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
    def element_model(self):
        return self.type_info["element_model"]

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
    def _update_element(self, element, request):
        try:
            replacement_element_id = request.data["element"]["id"]
            replacement_element_type = request.data["element"]["type"]
        except KeyError:
            raise ParseError(detail="Must provide a dict 'element' with id and type")

        new_type = TYPE_MAPPING[replacement_element_type]
        replacement_element_model = new_type["element_model"]
        replacement_synonym_model = new_type["synonym_model"]

        try:
            replacement_element = replacement_element_model.objects.get(pk=replacement_element_id)
        except replacement_element_model.DoesNotExist:
            raise ParseError(detail=f"No {self.element_type} exists with id {replacement_element_id}")

        if replacement_element_type != self.element_type:
            additional_fields = request.data.get("additional_fields", {})
            replacement_declaration_model = new_type["model"]
            old_fields = [field.name for field in self.type_model._meta.get_fields()]
            new_fields = [field.name for field in replacement_declaration_model._meta.get_fields()]
            same_fields = set(old_fields).intersection(set(new_fields))

            new_declared_element_fields = (
                additional_fields  # TODO: should there be a limit to which fields are overrideable?
            )
            for field in same_fields:
                new_declared_element_fields[field] = getattr(element, field)
                # TODO: this means existing same fields would override provided fields

            if self.element_type != "microorganism" and replacement_element_type == "microorganism":
                new_declared_element_fields["new_species"] = element.new_name
            elif self.element_type == "microorganism" and replacement_element_type != "microorganism":
                new_declared_element_fields["new_name"] = element.new_name

            new_declared_element_fields["id"] = None

            # utiliser le serializer pour comprendre les valeurs complexes comme used_part
            new_element = new_type["serializer"](data=new_declared_element_fields)
            new_element.is_valid(raise_exception=True)
            # le serializer a besoin d'un id et non pas l'objet
            new_element.validated_data["declaration"] = element.declaration
            # pour reutiliser le serializer, faut mettre les données de l'element dans ce format
            new_element.validated_data[replacement_element_type] = {"id": replacement_element.id}
            new_element = new_element.create(new_element.validated_data)
            element.delete()
            element = new_element
        else:
            setattr(element, self.element_type, replacement_element)
        element.request_status = self.type_model.AddableStatus.REPLACED
        element.new = False

        synonyms = request.data.get("synonyms", [])
        for synonym in synonyms:
            if not synonym.get("id"):
                # add new synonym
                try:
                    name = synonym.get("name")
                except KeyError:
                    raise ParseError(detail="Must provide 'name' to create new synonym")
                replacement_synonym_model.objects.create(standard_name=replacement_element, name=name)

        return element
