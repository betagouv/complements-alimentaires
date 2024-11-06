from rest_framework.generics import ListAPIView
from data.models import DeclaredPlant
from api.serializers import DeclaredPlantSerializer


class DeclaredIngredientsView(ListAPIView):
    serializer_class = DeclaredPlantSerializer

    def get_queryset(self):
        return DeclaredPlant.objects.all()
        # return list(itertools.chain(Tweet.objects.all(), Article.objects.all()))
