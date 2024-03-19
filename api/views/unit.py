from rest_framework.generics import ListAPIView
from data.models import SubstanceUnit
from api.serializers import SubstanceUnitSerializer


class UnitListView(ListAPIView):
    model = SubstanceUnit
    serializer_class = SubstanceUnitSerializer
