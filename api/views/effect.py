from rest_framework.generics import ListAPIView

from api.serializers import EffectSerializer
from data.models import Effect


class EffectListView(ListAPIView):
    model = Effect
    serializer_class = EffectSerializer
    queryset = Effect.objects.filter(missing_import_data=False)
