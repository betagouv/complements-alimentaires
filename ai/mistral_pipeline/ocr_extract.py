# ingredients list extraction from mistral
# https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/ocr/data_extraction.ipynb#scrollTo=FZdL0ZXYkO0n
from .client import client
import json
from mistralai.extra import response_format_from_pydantic_model
from pydantic import BaseModel, Field
import requests
from pypdf import PdfReader
from io import BytesIO


# TODO: consider security measures like limiting the size of pdf read or number of pages processed
# TODO: consider calling the mistral per-page rather than per-file and stopping once a french list is found
def extract_pdf_text(url):
    response = requests.get(url)
    my_raw_data = response.content
    text = ""
    with BytesIO(my_raw_data) as data:
        read_pdf = PdfReader(data)
        for page in read_pdf.pages:
            text += page.extract_text()
    return text


def extract_lists_from_text(text):
    completion_args = {
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 1,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "response_schema",
                "schema": {
                    "properties": {
                        "ingredients_lists": {
                            "items": {
                                "properties": {
                                    "ingredients": {
                                        "description": "a list of ingredients present in the text. Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that.",
                                        "type": "array",
                                    },
                                    "language": {
                                        "description": "the language the list is written in, in ISO 639-1 format",
                                        "type": "string",
                                    },
                                    "list_type": {"description": "'list' or 'composition'", "type": "string"},
                                },
                                "required": ["language", "ingredients", "list_type"],
                                "type": "object",
                            },
                            "type": "array",
                        }
                    },
                    "required": ["ingredients"],
                    "type": "object",
                },
            },
        },
    }

    response = client.beta.conversations.start(
        inputs=[{"role": "user", "content": text}],
        model="mistral-medium-latest",
        instructions="The user will send you text extracted from a PDF file. Please respond with a list of ingredients present in the text.",
        completion_args=completion_args,
        tools=[],
    )
    return json.loads(response.outputs[0].content)


def extract_lists_from_pdf(url):
    text = extract_pdf_text(url)
    if not text:
        return
    return extract_lists_from_text(text)


class IngredientsList(BaseModel):
    language: str = Field(..., description="the language the list is written in, in ISO 639-1 format")
    # TODO: make ingredients description configurable for prompt tweaking
    ingredients: list[str] = Field(
        ...,
        description="a list of ingredients present in the file. Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that.",
    )
    list_type: str = Field(..., description="'list' or 'composition'")


class Document(BaseModel):
    ingredients_lists: list[IngredientsList]


def extract_lists(url):
    # accepts image (inc gif), and pdf
    response = client.ocr.process(
        model="mistral-ocr-4-0",  # TODO: is this configurable?
        document={"type": "document_url", "document_url": url},
        document_annotation_format=response_format_from_pydantic_model(Document),
        include_image_base64=False,
        extract_header=False,
        extract_footer=False,
        confidence_scores_granularity="page",
    )

    # Convert response to JSON format
    response_dict = json.loads(response.model_dump_json())
    # of interest: response[pages][0][confidence_scores][average_page_confidence_score/minimum_page_confidence_score]
    # response[usage_info]
    return json.loads(response_dict["document_annotation"])


def get_french_list(ingredients_lists):
    for ing_list in ingredients_lists:
        if ing_list["language"] == "fr":
            return ing_list["ingredients"]
    print("No french list detected!")
    return []
