import os
import json
import math
import copy
from random import randrange

from django.utils import timezone

from data.models import Declaration, Attachment
from ai.mistral_pipeline.ocr_extract import extract_lists, extract_lists_from_pdf
from ai.mistral_pipeline.clean_ingredients import clean_ingredient_list

# ------- Misc helpers

CONFIGURATION = {
    "declarations_filter": {
        "article": Declaration.Article.ARTICLE_15,
        "status": Declaration.DeclarationStatus.AUTHORIZED,
        "teleicare_declaration_number__isnull": True,
        "modification_date__year": 2026,
    },
    "declarations_count": 10,
    # "dummy_extract": [
    #     [{"language": "fr", "ingredients": ["essaye"]}, {"language": "es", "ingredients": "prueba"}],
    #     [{"language": "en", "ingredients": ["test"]}, {"language": "fr", "ingredients": ["encore"]}]
    # ],
    # "dummy_clean": ["test", "clean"],
    "ocr": {
        "model": "mistral-ocr-4-0",
        "ingredients_description": "a list of ingredients present in the file. Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that.",
        "list_type_description": "'list' or 'composition'",
    },
    "pdf_text": {
        "model": "mistral-medium-latest",
        "instructions": "The user will send you text extracted from a PDF file. Please respond with a list of ingredients present in the text.",
        "ingredients_description": "a list of ingredients present in the text. Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that.",
        "list_type_description": "'list' or 'composition'",
    },
    "clean": {
        "model": "mistral-medium-latest",
        "instructions": "Given a series of strings by the user, return an object with a key 'ingredients' with an array of the ingredient names.\nWhere a scientific name is given, return only the scientific name.",
    },
}


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename):
    data = None
    with open(f"{filename}", encoding="utf-8") as f:
        data = json.load(f)
    return data


# this function merges a list of dicts into one dict,
# ensuring ingredients are not lost if there are shared keys
# this also restructures the langauge lists so that the language is a key and the list a value
def merge_lists(ingredients_lists):
    merged = {"list": {}, "composition": {}}
    for extraction in ingredients_lists:
        for language_result in extraction:
            # TODO: handle potentially malformatted responses?
            lang = language_result["language"]
            value = language_result["ingredients"]
            list_type = language_result["list_type"]
            if lang not in merged[list_type]:
                merged[list_type][lang] = copy.deepcopy(value)
            else:
                merged[list_type][lang] += value
    # deduplicate
    for list_type, merged_lists in merged.items():
        for lang, value in merged_lists.items():
            merged_lists[lang] = list(set(merged_lists[lang]))
    return merged["list"] if merged["list"] else merged["composition"]


def save_error(results, error):
    if "errors" not in results:
        results["errors"] = []
    results["errors"].append(error)


# ------- Extract data


def get_declarations(configuration):
    count = configuration["declarations_count"] or 10
    return Declaration.objects.filter(**configuration["declarations_filter"]).order_by("?")[:count]


# return a list of extracted ingredients from all associated LABEL files
# NB: we do not handle conflicting dict keys here
def extract_ingredients(configuration, results, declaration):
    if "dummy_extract" in configuration:
        return configuration["dummy_extract"]

    labels = declaration.attachments.filter(type=Attachment.AttachmentType.LABEL)
    ingredients_lists = []
    results["attachments"] = []
    results["readable_pdfs"] = []
    results["obligatory_mentions"] = []
    for label in labels:
        # TODO: handle possibility of l.file is None
        url = f"{os.getenv('MEDIA_ROOT_URL')}{label.file.url}"
        new_lists = []
        extraction = None

        # PDFs that are searchable are better parsed via text
        # rather than Mistral's Document AI
        if url.endswith(".pdf"):
            try:
                config = configuration["pdf_text"] if "pdf_text" in configuration else {}
                extraction = extract_lists_from_pdf(url, **config)
                if extraction and "ingredients_lists" in extraction and extraction["ingredients_lists"]:
                    pdf_lists = extraction["ingredients_lists"]
                    new_lists.append(pdf_lists)
                    results["readable_pdfs"].append(url)
            except Exception as e:
                message = f"Error extracting list for pdf label {url}"
                print(message)
                save_error(results, {"message": message, "error": str(e)})

        # fallback to OCR for images or non searchable PDFs
        if not new_lists:
            try:
                config = configuration["ocr"] if "ocr" in configuration else {}
                extraction = extract_lists(url, **config)
                new_lists.append(extraction["ingredients_lists"])
                results["attachments"].append(url)
            except Exception as e:
                message = f"Error extracting list for label {url}"
                print(message)
                save_error(results, {"message": message, "error": str(e)})
        if new_lists:
            ingredients_lists += new_lists
        if "obligatory_mentions" in extraction:
            results["obligatory_mentions"].append(extraction["obligatory_mentions"])
    return ingredients_lists


# d for declaration
def save_declaration_details(results, d):
    results["article"] = d.article
    results["status"] = d.status
    declared_ingredients = []
    ing_types = ["ingredient", "plant", "microorganism", "substance"]
    for type in ing_types:
        qs = getattr(d, f"declared_{type}s")
        declared_ingredients += list(qs.values_list(f"{type}__name", flat=True))
    results["declared_ingredients_count"] = len(declared_ingredients)
    results["declared_ingredients"] = declared_ingredients
    results["computed_substances"] = list(d.computed_substances.values_list("substance__name", flat=True))
    results["total_ingredients_count"] = results["declared_ingredients_count"] + len(results["computed_substances"])
    # TODO: save declaration URL for ease of checking?


def save_extracted_lists_stats(results, ingredients_lists):
    # check difference in extracted lists counts
    max_count = 0
    max_lang = ""
    min_count = None
    min_lang = ""
    extracted_differential = None
    for lang, list in ingredients_lists.items():
        list_count = len(list)
        if list_count > max_count:
            max_count = list_count
            max_lang = lang
        if min_count is None or list_count < min_count:
            min_count = list_count
            min_lang = lang
    # if there are no ingredients lists, then min count never gets set
    if min_count is not None:
        extracted_differential = max_count - min_count
        results["max_difference_extracted_counts"] = extracted_differential
    if extracted_differential:
        results["extracted_count_extremes"] = {
            "min": min_count,
            "max": max_count,
            "min_lang": min_lang,
            "max_lang": max_lang,
        }


def pick_list(results, ingredients_lists):
    # pick the ingredients list for comparison
    ingredients_list = None
    if "fr" in ingredients_lists:
        ingredients_list = ingredients_lists["fr"]
        results["list_lang"] = "fr"
    else:
        # if there isn't a list in French, return any other list language randomly
        keys = list(ingredients_lists.keys())
        if not keys:
            print("No keys!", ingredients_lists)
            save_error(results, {"message": "No list found"})
            return []
        random_language = keys[randrange(len(keys))]
        ingredients_list = ingredients_lists[random_language]
        results["list_lang"] = random_language
    return ingredients_list


def clean_list(configuration, results, ingredients_list):
    if "dummy_clean" in configuration:
        return configuration["dummy_clean"]
    cleaned_list = ingredients_list
    try:
        config = configuration["clean"] if "clean" in configuration else {}
        cleaned_list = clean_ingredient_list(ingredients_list, **config)
    except Exception as e:
        message = "Error cleaning list"
        print(message)
        save_error(results, {"message": message, "error": str(e)})
    results["cleaned_list"] = cleaned_list
    return cleaned_list


def save_differential(results):
    results["declared_ingredient_count_difference"] = results["list_count"] - results["declared_ingredients_count"]
    results["total_ingredient_count_difference"] = results["list_count"] - results["total_ingredients_count"]


def calculate_trust_score(results):
    trust = 1
    # does the declaration only have one declared ingredient?
    declared_count = results["declared_ingredients_count"]
    declared_difference_count = results["declared_ingredient_count_difference"]
    if declared_difference_count > 0:
        # declarations with one ingredient are suspicious,
        # expontentially worse with every missed ingredient
        exponent = 2 if declared_count == 1 else 1
        trust -= (declared_difference_count ^ exponent) * 0.1
    # how is it on obligatory mentions?
    obligatory_mentions = {}
    for page in results["obligatory_mentions"]:
        for key, value in page.items():
            obligatory_mentions[key] = value or obligatory_mentions.get(key, False)
    mention_score = 0
    for mention, value in obligatory_mentions.items():
        mention_score += 1 if value else 0
    max_score = len(obligatory_mentions.keys())
    if not max_score:
        print("No obligatory mentions detected!")
    else:
        trust -= (max_score - mention_score) / max_score
    results["trust"] = max(trust, 0)


def generate_data(configuration):
    data = {
        "configuration": configuration,
        "declarations": {},
    }
    declarations = get_declarations(configuration)
    for d in declarations:
        print("Declaration", d.id)
        declaration_results = {}
        save_declaration_details(declaration_results, d)

        # get all ingredients present in the attachments
        ingredients_lists = extract_ingredients(configuration, declaration_results, d)
        declaration_results["extracted_ingredients"] = ingredients_lists
        merged_ingredients_lists = merge_lists(ingredients_lists)
        save_extracted_lists_stats(declaration_results, merged_ingredients_lists)

        # choose the ingredients list we will use for comparison with the declared
        chosen_list = pick_list(declaration_results, merged_ingredients_lists)
        cleaned_list = clean_list(configuration, declaration_results, chosen_list)
        declaration_results["list_count"] = len(cleaned_list)
        save_differential(declaration_results)
        calculate_trust_score(declaration_results)

        # finally, save the results
        data["declarations"][d.id] = declaration_results
    return data


# ------- Summarise data


def difference(values):
    difference = {"count": len(values)}
    difference["mean"] = sum(values) / difference["count"]
    sorted_list = sorted(values)
    median_index = math.floor(len(sorted_list) / 2)
    difference["median"] = sorted_list[median_index]
    # maybe these ideally have ids to make it easier to find the decla
    difference["max_over"] = sorted_list[-1]
    difference["max_under"] = sorted_list[0]
    difference["over"] = {"count": len([x for x in values if x > 0])}
    difference["under"] = {"count": len([x for x in values if x < 0])}
    difference["exact"] = {"count": len([x for x in values if x == 0])}
    return difference


# here, results is the higher level dict unlike methods above
# which are per-declaration
def summarise(results):
    declarations = results["declarations"]
    # ids = [] # ids may be necessary for debugging groupings
    declared_differences = []
    total_differences = []
    # could build other lists by grouping
    ids_lang_differences = []
    ids_non_french = []
    trust_threshold = 0.5
    low_trust = []
    for id, d in declarations.items():
        declared_differences.append(d["declared_ingredient_count_difference"])
        total_differences.append(d["total_ingredient_count_difference"])
        if "max_difference_extracted_counts" in d and d["max_difference_extracted_counts"]:
            ids_lang_differences.append(id)
        if "list_lang" in d and d["list_lang"] != "fr":
            ids_non_french.append(id)
        if d.get("trust", 1) < trust_threshold:
            low_trust.append(id)
    summary = {
        "configuration": results["configuration"],
        "declared": difference(declared_differences),
        "total": difference(total_differences),
        "lang_differences": ids_lang_differences,
        "non_french_declarations": ids_non_french,
        "low_trust": low_trust,
        # later could add per-article, language or other groupings
    }
    return summary


# ------- main
# To run these methods:
# - ensure MEDIA_ROOT_URL is set in local env vars
# - get details of or create read only database user for db in question
# - update env vars to the remote database and read only user details
# - ensure the directory ai/scripts/results exists
# - open a shell
# - import ai.scripts.difference_count as s
# - s.run_complete() or s.summarise(<filename without extension>)


def run_complete(**kwargs):
    folder = "ai/scripts/results"
    datetime = str(timezone.now())
    filename = f"{folder}/{datetime}"
    config = {**CONFIGURATION, **kwargs}
    data = generate_data(config)
    save_json(filename, data)
    # in theory, could add extra step to parse a json file to feed to this
    results = summarise(data)
    save_json(f"{filename}_summary", results)


def summarise_from_file(filename):
    data = load_json(f"{filename}.json")
    results = summarise(data)
    save_json(f"{filename}_summary", results)
