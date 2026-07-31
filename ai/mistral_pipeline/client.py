from django.conf import settings
from mistralai.client import Mistral

client = Mistral(api_key=settings.MISTRAL_API_KEY)
