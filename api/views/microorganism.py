from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import MicroorganismSerializer, MicroorganismModificationSerializer
from data.models import Microorganism

from .utils import IngredientRetrieveView
from ..permissions import IsInstructor


class MicroorganismRetrieveView(IngredientRetrieveView):
    model = Microorganism
    queryset = Microorganism.objects.filter(missing_import_data=False)
    serializer_class = MicroorganismSerializer


class MicroorganismCreateView(CreateAPIView):
    model = Microorganism
    queryset = Microorganism.objects.all()
    serializer_class = MicroorganismModificationSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
