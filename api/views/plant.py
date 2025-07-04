from rest_framework.generics import CreateAPIView, ListAPIView

from api.serializers import PlantFamilySerializer, PlantModificationSerializer, PlantPartSerializer, PlantSerializer
from data.models import Plant, PlantFamily, PlantPart

from ..permissions import IsInstructor
from .utils import IngredientRetrieveUpdateView


class PlantRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Plant
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    modification_serializer_class = PlantModificationSerializer


class PlantPartListView(ListAPIView):
    model = PlantPart
    queryset = PlantPart.objects.all()
    serializer_class = PlantPartSerializer


class PlantFamilyListView(ListAPIView):
    model = PlantFamily
    queryset = PlantFamily.objects.all()
    serializer_class = PlantFamilySerializer


class PlantCreateView(CreateAPIView):
    model = Plant
    queryset = Plant.objects.all()
    serializer_class = PlantModificationSerializer
    permission_classes = [IsInstructor]
