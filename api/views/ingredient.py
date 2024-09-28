from api.serializers import IngredientSerializer
from data.models import Ingredient

from .utils import IngredientRetrieveView


class IngredientRetrieveView(IngredientRetrieveView):
    model = Ingredient
    queryset = Ingredient.objects.filter(missing_import_data=False)
    serializer_class = IngredientSerializer
