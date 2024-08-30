from rest_framework.generics import ListAPIView

from api.serializers import GalenicFormulationSerializer
from data.models import GalenicFormulation


class GalenicFormulationListView(ListAPIView):
    model = GalenicFormulation
    serializer_class = GalenicFormulationSerializer
    queryset = GalenicFormulation.objects.filter(missing_import_data=False)
