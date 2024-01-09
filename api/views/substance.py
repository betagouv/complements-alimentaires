from rest_framework.generics import RetrieveAPIView
from data.models import Substance
from api.serializers import SubstanceSerializer


class SubstanceRetrieveView(RetrieveAPIView):
    model = Substance
    queryset = Substance.objects.all()
    serializer_class = SubstanceSerializer
