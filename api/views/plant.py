from rest_framework.generics import ListAPIView, CreateAPIView

from api.serializers import PlantPartSerializer, PlantSerializer, PlantModificationSerializer, PlantFamilySerializer
from data.models import Plant, PlantPart, PlantFamily

from .utils import IngredientRetrieveUpdateView
from ..permissions import IsInstructor


class PlantRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Plant
    queryset = Plant.objects.filter(missing_import_data=False)
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
