from rest_framework.generics import ListAPIView
from data.models import Effect
from api.serializers import EffectSerializer


class EffectListView(ListAPIView):
    model = Effect
    serializer_class = EffectSerializer
    queryset = Effect.objects.filter(missing_import_data=False, siccrf_is_obsolete=False)
