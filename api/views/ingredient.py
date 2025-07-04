from rest_framework.generics import CreateAPIView

from api.serializers import IngredientModificationSerializer, IngredientSerializer
from data.models import Ingredient

from ..permissions import IsInstructor
from .utils import IngredientRetrieveUpdateView


class IngredientRetrieveUpdateView(IngredientRetrieveUpdateView):
    model = Ingredient
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    modification_serializer_class = IngredientModificationSerializer


class IngredientCreateView(CreateAPIView):
    model = Ingredient
    queryset = Ingredient.objects.all()
    serializer_class = IngredientModificationSerializer
    permission_classes = [IsInstructor]
