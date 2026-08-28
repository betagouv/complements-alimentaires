from django.conf import settings
from mistralai.client import Mistral

client = Mistral(api_key=settings.MISTRAL_API_KEY)


# the API takes a json schema wrapped in this envelope, whether it is given to
# the OCR endpoint as a document annotation format or to a conversation as a
# response format
def add_format_boilerplate(schema):
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "response_schema",
            "schema": schema,
        },
    }
