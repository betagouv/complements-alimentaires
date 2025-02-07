from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import SubstanceSerializer, SubstanceModificationSerializer
from data.models import Substance

from .utils import IngredientRetrieveView
from ..permissions import IsInstructor


class SubstanceRetrieveView(IngredientRetrieveView):
    model = Substance
    queryset = Substance.objects.filter(missing_import_data=False)
    serializer_class = SubstanceSerializer


class SubstanceCreateView(CreateAPIView):
    model = Substance
    queryset = Substance.objects.all()
    serializer_class = SubstanceModificationSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
