import factory
from data.models import Webinar
import pytz


class WebinarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Webinar

    title = factory.Faker("catch_phrase")
    tagline = factory.Faker("paragraph")
    start_date = factory.Faker("future_datetime", tzinfo=pytz.timezone("Europe/Paris"))
    end_date = factory.Faker("future_datetime", tzinfo=pytz.timezone("Europe/Paris"))
    link = factory.Faker("uri")
