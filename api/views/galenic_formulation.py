from rest_framework.generics import ListAPIView
from data.models import GalenicFormulation
from api.serializers import GalenicFormulationSerializer


class GalenicFormulationListView(ListAPIView):
    model = GalenicFormulation
    serializer_class = GalenicFormulationSerializer
    queryset = GalenicFormulation.objects.filter(missing_import_data=False, siccrf_is_obsolete=False)
