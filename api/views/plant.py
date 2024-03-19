from rest_framework.generics import RetrieveAPIView, ListAPIView
from data.models import Plant, PlantPart
from api.serializers import PlantSerializer, PlantPartSerializer


class PlantRetrieveView(RetrieveAPIView):
    model = Plant
    queryset = Plant.objects.filter(missing_import_data=False)
    serializer_class = PlantSerializer


class PlantPartListView(ListAPIView):
    model = PlantPart
    queryset = PlantPart.objects.all()
    serializer_class = PlantPartSerializer
