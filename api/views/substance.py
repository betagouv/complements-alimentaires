from rest_framework.generics import CreateAPIView

from api.serializers import SubstanceSerializer, SubstanceModificationSerializer
from data.models import Substance

from .utils import IngredientRetrieveUpdateView
from ..permissions import IsInstructor


class SubstanceRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Substance
    # TODO: what's the deal with missing_import_data?
    queryset = Substance.objects.filter(missing_import_data=False)
    serializer_class = SubstanceSerializer
    modification_serializer_class = SubstanceModificationSerializer


class SubstanceCreateView(CreateAPIView):
    model = Substance
    queryset = Substance.objects.all()
    serializer_class = SubstanceModificationSerializer
    permission_classes = [IsInstructor]
