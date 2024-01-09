from rest_framework.generics import RetrieveAPIView
from data.models import Microorganism
from api.serializers import MicroorganismSerializer


class MicroorganismRetrieveView(RetrieveAPIView):
    model = Microorganism
    queryset = Microorganism.objects.all()
    serializer_class = MicroorganismSerializer
