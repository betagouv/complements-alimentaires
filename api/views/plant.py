from rest_framework.generics import RetrieveAPIView
from data.models import Plant
from api.serializers import PlantSerializer


class PlantRetrieveView(RetrieveAPIView):
    model = Plant
    queryset = Plant.objects.filter(missing_import_data=False)
    serializer_class = PlantSerializer
