# ingredients list extraction from mistral
# https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/ocr/data_extraction.ipynb#scrollTo=FZdL0ZXYkO0n
from .client import client
import json
from mistralai.extra import response_format_from_pydantic_model
from pydantic import BaseModel, Field


class IngredientsList(BaseModel):
    language: str = Field(..., description="the language the list is written in, in ISO 639-1 format")
    # TODO: make ingredients description configurable for prompt tweaking
    ingredients: list[str] = Field(
        ...,
        description="a list of ingredients present in the file. Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that.",
    )


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
