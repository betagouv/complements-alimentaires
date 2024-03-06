from rest_framework.generics import ListAPIView
from data.models import Population
from api.serializers import PopulationSerializer


class PopulationListView(ListAPIView):
    model = Population
    serializer_class = PopulationSerializer
    queryset = Population.objects.filter(missing_import_data=False, siccrf_is_obsolete=False)
