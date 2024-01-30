from rest_framework.generics import RetrieveAPIView
from data.models import Substance
from api.serializers import SubstanceSerializer


class SubstanceRetrieveView(RetrieveAPIView):
    model = Substance
    queryset = Substance.objects.filter(missing_import_data=False)
    serializer_class = SubstanceSerializer
