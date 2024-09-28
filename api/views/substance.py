from api.serializers import SubstanceSerializer
from data.models import Substance

from .utils import IngredientRetrieveView


class SubstanceRetrieveView(IngredientRetrieveView):
    model = Substance
    queryset = Substance.objects.filter(missing_import_data=False)
    serializer_class = SubstanceSerializer
