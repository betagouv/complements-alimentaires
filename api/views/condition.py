from rest_framework.generics import ListAPIView
from data.models import Condition
from api.serializers import ConditionSerializer


class ConditionListView(ListAPIView):
    model = Condition
    serializer_class = ConditionSerializer
    queryset = Condition.objects.filter(missing_import_data=False, is_obsolete=False)
