from rest_framework.generics import CreateAPIView

from api.serializers import MicroorganismSerializer, MicroorganismModificationSerializer
from data.models import Microorganism

from .utils import IngredientRetrieveUpdateView
from ..permissions import IsInstructor


class MicroorganismRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Microorganism
    queryset = Microorganism.objects.filter(missing_import_data=False)
    serializer_class = MicroorganismSerializer
    modification_serializer_class = MicroorganismModificationSerializer


class MicroorganismCreateView(CreateAPIView):
    model = Microorganism
    queryset = Microorganism.objects.all()
    serializer_class = MicroorganismModificationSerializer
    permission_classes = [IsInstructor]
