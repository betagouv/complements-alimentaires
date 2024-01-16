from rest_framework.generics import RetrieveAPIView
from data.models import Plant
from api.serializers import PlantSerializer


class PlantRetrieveView(RetrieveAPIView):
    model = Plant
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
