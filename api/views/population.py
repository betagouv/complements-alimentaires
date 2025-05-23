from rest_framework.generics import ListAPIView

from api.serializers import PopulationSerializer
from data.models import Population


class PopulationListView(ListAPIView):
    model = Population
    serializer_class = PopulationSerializer
    queryset = Population.up_to_date_objects.filter(missing_import_data=False).order_by("name")
