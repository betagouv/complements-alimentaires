from api.serializers import WebinarSerializer
from data.models import Webinar
from django.utils import timezone
from rest_framework.generics import ListAPIView


class WebinarView(ListAPIView):
    model = Webinar
    serializer_class = WebinarSerializer
    queryset = Webinar.objects.filter(end_date__gt=timezone.now())
