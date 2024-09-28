from rest_framework.generics import ListAPIView

from api.serializers import PlantPartSerializer, PlantSerializer
from data.models import Plant, PlantPart

from .utils import IngredientRetrieveView


class PlantRetrieveView(IngredientRetrieveView):
    model = Plant
    queryset = Plant.objects.filter(missing_import_data=False)
    serializer_class = PlantSerializer


class PlantPartListView(ListAPIView):
    model = PlantPart
    queryset = PlantPart.objects.all()
    serializer_class = PlantPartSerializer
