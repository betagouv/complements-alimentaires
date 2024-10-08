from rest_framework.generics import ListAPIView

from api.serializers import PreparationSerializer
from data.models import Preparation


class PreparationListView(ListAPIView):
    model = Preparation
    serializer_class = PreparationSerializer
    queryset = Preparation.up_to_date_objects.filter(missing_import_data=False)
