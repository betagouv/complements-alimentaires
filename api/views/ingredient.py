from rest_framework.generics import RetrieveAPIView

from data.models import Ingredient
from api.serializers import IngredientSerializer


class IngredientRetrieveView(RetrieveAPIView):
    model = Ingredient
    queryset = Ingredient.objects.filter(missing_import_data=False)
    serializer_class = IngredientSerializer
