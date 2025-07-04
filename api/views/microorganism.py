from rest_framework.generics import CreateAPIView

from api.serializers import MicroorganismModificationSerializer, MicroorganismSerializer
from data.models import Microorganism

from ..permissions import IsInstructor
from .utils import IngredientRetrieveUpdateView


class MicroorganismRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Microorganism
    queryset = Microorganism.objects.all()
    serializer_class = MicroorganismSerializer
    modification_serializer_class = MicroorganismModificationSerializer


class MicroorganismCreateView(CreateAPIView):
    model = Microorganism
    queryset = Microorganism.objects.all()
    serializer_class = MicroorganismModificationSerializer
    permission_classes = [IsInstructor]
