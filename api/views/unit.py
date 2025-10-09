from rest_framework.generics import ListAPIView

from api.serializers import UnitSerializer
from data.models import Unit


class UnitListView(ListAPIView):
    model = Unit
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
