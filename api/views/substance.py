from rest_framework.generics import CreateAPIView

from api.serializers import SubstanceModificationSerializer, SubstanceSerializer
from data.models import Substance

from ..permissions import IsInstructor
from .utils import IngredientRetrieveUpdateView


class SubstanceRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Substance
    queryset = Substance.objects.all()
    serializer_class = SubstanceSerializer
    modification_serializer_class = SubstanceModificationSerializer


class SubstanceCreateView(CreateAPIView):
    model = Substance
    queryset = Substance.objects.all()
    serializer_class = SubstanceModificationSerializer
    permission_classes = [IsInstructor]
