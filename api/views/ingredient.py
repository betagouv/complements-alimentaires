from rest_framework.generics import CreateAPIView

from api.serializers import IngredientSerializer, IngredientModificationSerializer
from data.models import Ingredient

from .utils import IngredientRetrieveUpdateView
from ..permissions import IsInstructor


class IngredientRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Ingredient
    queryset = Ingredient.objects.filter(missing_import_data=False)
    serializer_class = IngredientSerializer
    modification_serializer_class = IngredientModificationSerializer


class IngredientCreateView(CreateAPIView):
    model = Ingredient
    queryset = Ingredient.objects.all()
    serializer_class = IngredientModificationSerializer
    permission_classes = [IsInstructor]
