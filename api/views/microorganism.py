from api.serializers import MicroorganismSerializer
from data.models import Microorganism

from .utils import IngredientRetrieveView


class MicroorganismRetrieveView(IngredientRetrieveView):
    model = Microorganism
    queryset = Microorganism.objects.filter(missing_import_data=False)
    serializer_class = MicroorganismSerializer
