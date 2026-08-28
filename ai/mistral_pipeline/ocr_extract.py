# ingredients list extraction from mistral
# https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/ocr/data_extraction.ipynb#scrollTo=FZdL0ZXYkO0n
from .client import client, add_format_boilerplate
from .throttle import throttled
import json
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


@throttled
def extract_lists_from_text(
    text,
    model="mistral-medium-latest",
    instructions="The user will send you text extracted from a PDF file. Please respond with a list of ingredients present in the text.",
    ingredients_description="a list of ingredients present in the text. Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that.",
    list_type_description="'list' or 'composition'",
    # extracting a list is a deterministic task, a creative model invents ingredients
    temperature=0.1,
):
    schema = {
        "properties": {
            "ingredients_lists": {
                "items": {
                    "properties": {
                        "ingredients": {
                            "description": ingredients_description,
                            "type": "array",
                        },
                        "language": {
                            "description": "the language the list is written in, in ISO 639-1 format",
                            "type": "string",
                        },
                        "list_type": {"description": list_type_description, "type": "string"},
                    },
                    "required": ["language", "ingredients", "list_type"],
                    "type": "object",
                },
                "type": "array",
            }
        },
        "required": ["ingredients_lists"],
        "type": "object",
    }
    completion_args = {
        "temperature": temperature,
        "max_tokens": 2048,
        "top_p": 1,
        "response_format": add_format_boilerplate(schema),
    }
    response = client.beta.conversations.start(
        inputs=[{"role": "user", "content": text}],
        model=model,
        instructions=instructions,
        completion_args=completion_args,
        tools=[],
    )
    return json.loads(response.outputs[0].content)


def extract_lists_from_pdf(url, **kwargs):
    text = extract_pdf_text(url)
    # sometimes have only whitespace in the string,
    # so make sure to remove that before checking if we have output
    if text:
        text = text.strip()
    if not text:
        return
    return extract_lists_from_text(text, **kwargs)


@throttled
def extract_lists(
    url,
    model="mistral-ocr-4-0",
    ingredients_description="a list of ingredients present in the file. Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that.",
    list_type_description="'list' or 'composition'",
):
    schema = {
        "properties": {
            "ingredients_lists": {
                "items": {
                    "properties": {
                        "ingredients": {
                            "description": ingredients_description,
                            "type": "array",
                        },
                        "language": {
                            "description": "the language the list is written in, in ISO 639-1 format",
                            "type": "string",
                        },
                        "list_type": {"description": list_type_description, "type": "string"},
                    },
                    "required": ["language", "ingredients", "list_type"],
                    "type": "object",
                },
                "type": "array",
            }
        },
        "required": ["ingredients_lists"],
        "type": "object",
    }
    response_format = add_format_boilerplate(schema)
    # accepts image (inc gif), and pdf
    response = client.ocr.process(
        model=model,
        document={"type": "document_url", "document_url": url},
        document_annotation_format=response_format,
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
