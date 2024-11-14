from rest_framework.generics import ListAPIView

from api.serializers import ConditionSerializer
from data.models import Condition


class ConditionListView(ListAPIView):
    model = Condition
    serializer_class = ConditionSerializer
    queryset = Condition.up_to_date_objects.filter(missing_import_data=False).order_by("name")
