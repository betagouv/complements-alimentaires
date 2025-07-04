from rest_framework.generics import ListAPIView

from api.serializers import GalenicFormulationSerializer
from data.models import GalenicFormulation


class GalenicFormulationListView(ListAPIView):
    model = GalenicFormulation
    serializer_class = GalenicFormulationSerializer
    queryset = GalenicFormulation.up_to_date_objects.all()
