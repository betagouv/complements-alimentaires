# https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/ocr/data_extraction.ipynb#scrollTo=6yOKFR6XlnnC
# first import needed updating
# file path is relative to where the command is run from
# python manage.py shell < notes/2026/extract_label.py
from django.conf import settings
from mistralai.client import Mistral
import base64
import json
from pydantic import BaseModel, Field
from mistralai.extra import response_format_from_pydantic_model
from api.utils.search import search_elements
import re
from rest_framework import status
from rest_framework.generics import GenericAPIView
from api.permissions import IsDeclarationAuthor
from rest_framework.response import Response
from data.models import Declaration, Attachment

api_key = settings.MISTRAL_API_KEY
client = Mistral(api_key=api_key)


def encode_pdf(pdf_path):
    """Encode the pdf to base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None


# class ImageType(str, Enum):
#     GRAPH = "graph"
#     TEXT = "text"
#     TABLE = "table"
#     IMAGE = "image"

# class Image(BaseModel):
#     image_type: ImageType = Field(..., description="The type of the image. Must be one of 'graph', 'text', 'table' or 'image'.")
#     description: str = Field(..., description="A description of the image.")


class Ingredient(BaseModel):
    name: str = Field(..., description="Le nom de l'ingrédient")
    quantity: float | None = Field(None, description="La quantitié de l'ingrédient, si indiquée")
    unit: str | None = Field(
        None, description="La unité pour la quantité de l'ingrédient, si la quantité est indiquée"
    )
    purpose: str | None = Field(None, description="Le but de l'ingrédient dans la composition, si indiqué")
    preparation: str | None = Field(
        None, description="La manière de préparation de l'ingrédient, si indiqué. Exemples : 'extrait sec'"
    )
    plant_part: str | None = Field(None, description="La partie de la plante utilisée, si indiqué")


class Document(BaseModel):
    languages: list[str] = Field(
        ..., description="Les langages presents dans l'étiquette en format ISO 639-1 (e.g., 'en', 'fr')."
    )
    product_name: str = Field(..., description="Le nom du produit")
    composition: list[Ingredient] = Field(
        ...,
        description="La composition du produit, la liste d'ingrédients avec leur quantité. Inclure que les ingrédients écrits en français",
    )
    galenic_form: str = Field(..., description="La forme galénique du produit")
    # ingredient_list: list[str] = Field(..., description="Les noms d'ingrédients dans le produit")
    target_population: list[str | None] = Field(
        ..., description="La ou les populations auxquelles le produit est déstiné"
    )
    risk_population: list[str | None] = Field(
        ..., description="La ou les populations ou les conditions auxquelles le produit est déconseillé"
    )


def extract_structured_data(attachment_path):
    # pdf_path = "notes/2026/labels/celine.pdf"
    base64_pdf = encode_pdf(attachment_path)
    # base64_document = request.data.get("base64Document")
    base64_url = f"data:application/pdf;base64,{base64_pdf}"

    annotations_response = client.ocr.process(
        model="mistral-ocr-latest",
        pages=list(
            range(8)
        ),  # Document Annotations has a limit of 8 pages, we recommend spliting your documents when using it; bbox annotations does not have the same limit
        document={"type": "document_url", "document_url": base64_url},
        document_annotation_format=response_format_from_pydantic_model(Document),
        include_image_base64=False,  # We are not interested on retrieving the bbox images in this example, only their annotations
    )

    data = annotations_response.document_annotation
    return json.loads(data)


def match_ingredient(ingredient):
    search_results = search_elements({"term": ingredient})
    if not search_results:
        normalised_name = re.sub(r"[®*]", "", ingredient)
        search_results = search_elements({"term": normalised_name})
    if not search_results:
        match = re.match(r"(.+?) \((.+)\)", normalised_name)
        if match:
            first_name = match.group(1)
            search_results = search_elements({"term": first_name})
            second_name = match.group(2)
            search_results += search_elements({"term": second_name})
    unique_results = list(set(search_results))
    serialized_results = []
    for result in unique_results:
        serialized_results.append({"id": result.id, "type": result.object_type, "name": result.name})
    return serialized_results


def match_ingredients(ingredients):
    results = {}
    one_result = []
    zero_results = []
    multiple_results = []

    for ingredient in ingredients:
        serialized_results = match_ingredient(ingredient)
        results[ingredient] = {"results": serialized_results, "count": len(serialized_results)}
        if len(serialized_results) == 1:
            one_result.append(ingredient)
        elif len(serialized_results) == 0:
            zero_results.append(ingredient)
        else:
            multiple_results.append(ingredient)

    print(results)
    print("one result", len(one_result))
    print("zero results", len(zero_results))
    print("multiple", len(multiple_results))
    return results


class ExtractLabelView(GenericAPIView):
    permission_classes = [IsDeclarationAuthor]
    queryset = Declaration

    def get(self, request, *args, **kwargs):
        declaration = self.get_object()
        label = declaration.attachments.filter(type=Attachment.AttachmentType.LABEL).first()
        if not label:
            return Response("Must upload label", status=status.HTTP_400_BAD_REQUEST)
        json_data = extract_structured_data(label.file.path)
        ingredient_list = list(map(lambda x: x["name"], json_data["composition"]))
        results = match_ingredients(ingredient_list)
        return Response({"extraction": json_data, "results": results}, status=status.HTTP_200_OK)
