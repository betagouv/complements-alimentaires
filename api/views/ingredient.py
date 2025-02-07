from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import IngredientSerializer, IngredientModificationSerializer
from data.models import Ingredient

from .utils import IngredientRetrieveView
from ..permissions import IsInstructor


class IngredientRetrieveView(IngredientRetrieveView):
    model = Ingredient
    queryset = Ingredient.objects.filter(missing_import_data=False)
    serializer_class = IngredientSerializer


class IngredientCreateView(CreateAPIView):
    model = Ingredient
    queryset = Ingredient.objects.all()
    serializer_class = IngredientModificationSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
