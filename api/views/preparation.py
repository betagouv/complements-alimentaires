from rest_framework.generics import ListAPIView

from api.serializers import PreparationSerializer
from data.models import Preparation


class PreparationListView(ListAPIView):
    model = Preparation
    serializer_class = PreparationSerializer
    queryset = Preparation.objects.filter(missing_import_data=False, siccrf_is_obsolete=False)
