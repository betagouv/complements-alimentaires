from api.serializers import WebinaireSerializer
from data.models import Webinaire
from django.utils import timezone
from rest_framework.generics import ListAPIView


class WebinairesView(ListAPIView):
    model = Webinaire
    serializer_class = WebinaireSerializer
    queryset = Webinaire.objects.filter(end_date__gt=timezone.now())
