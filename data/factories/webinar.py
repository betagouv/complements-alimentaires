import factory
from data.models import Webinar
from zoneinfo import ZoneInfo


class WebinarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Webinar

    title = factory.Faker("catch_phrase")
    tagline = factory.Faker("paragraph")
    start_date = factory.Faker("future_datetime", tzinfo=ZoneInfo("Europe/Paris"))
    end_date = factory.Faker("future_datetime", tzinfo=ZoneInfo("Europe/Paris"))
    link = factory.Faker("uri")
