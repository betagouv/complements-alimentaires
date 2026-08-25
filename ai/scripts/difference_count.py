import json
import math
from random import randrange
from django.utils import timezone

from data.models import Declaration

# ------- Misc helpers

CONFIGURATION = {
    "declarations_filter": {
        "article": Declaration.Article.ARTICLE_15,
        "status": Declaration.DeclarationStatus.AUTHORIZED,
    },
    "declarations_count": 5,
    # TODO: add details about the model
    "extract_ingredients": {"dummy": {"en": ["test", "sample", "etc"], "es": ["essaye", "sample"]}},
}


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename):
    data = None
    with open(f"{filename}", encoding="utf-8") as f:
        data = json.load(f)
    return data


# ------- Extract data


def get_declarations():
    configuration = CONFIGURATION
    count = configuration["declarations_count"] or 10
    return Declaration.objects.filter(**configuration["declarations_filter"])[:count]


def extract_ingredients(declaration):
    dummy_config = CONFIGURATION["extract_ingredients"]["dummy"]
    if dummy_config:
        return dummy_config
    # TODO: call mistral, maybe pass in configuration or reuse the same convo?
    return []


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


def save_extracted_lists_stats(results, ingredients_lists):
    # check difference in extracted lists counts
    max_count = 0
    max_lang = ""
    min_count = None
    min_lang = ""
    for lang, list in ingredients_lists.items():
        list_count = len(list)
        if list_count > max_count:
            max_count = list_count
            max_lang = lang
        if min_count is None or list_count < min_count:
            min_count = list_count
            min_lang = lang
    extracted_differential = max_count - min_count
    results["max_difference_extracted_counts"] = extracted_differential
    if extracted_differential:
        results["extracted_count_extremes"] = {
            "min": min_count,
            "max": max_count,
            "min_lang": min_lang,
            "max_lang": max_lang,
        }


def save_list_stats(results, ingredients_lists):
    # pick the ingredients list for comparison
    ingredients_list = None
    if "fr" in ingredients_lists:
        ingredients_list = ingredients_lists["fr"]
        results["list_lang"] = "fr"
    else:
        # if there isn't a list in French, return any other list language randomly
        keys = list(ingredients_lists.keys())
        random_language = keys[randrange(len(keys))]
        ingredients_list = ingredients_lists[random_language]
        results["list_lang"] = random_language
    results["list_count"] = len(ingredients_list)


def save_differential(results):
    results["declared_ingredient_count_difference"] = results["list_count"] - results["declared_ingredients_count"]
    results["total_ingredient_count_difference"] = results["list_count"] - results["total_ingredients_count"]


def generate_data():
    data = {
        "configuration": CONFIGURATION,
        "declarations": {},
    }
    declarations = get_declarations()
    for d in declarations:
        declaration_results = {}
        save_declaration_details(declaration_results, d)
        ingredients_lists = extract_ingredients(d)
        declaration_results["extracted_ingredients"] = ingredients_lists
        save_extracted_lists_stats(declaration_results, ingredients_lists)
        save_list_stats(declaration_results, ingredients_lists)
        save_differential(declaration_results)
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
    for id, d in declarations.items():
        declared_differences.append(d["declared_ingredient_count_difference"])
        total_differences.append(d["total_ingredient_count_difference"])
        if d["max_difference_extracted_counts"]:
            ids_lang_differences.append(id)
    summary = {
        "configuration": results["configuration"],
        "declared": difference(declared_differences),
        "total": difference(total_differences),
        "lang_differences": ids_lang_differences,
        # later could add per-article, language or other groupings
    }
    return summary


# ------- main
# To run these methods:
# - ensure the directory ai/scripts/results exists
# - open a shell
# - import ai.scripts.difference_count as s
# - s.run_complete() or s.summarise(<filename without extension>)


def run_complete():
    folder = "ai/scripts/results"
    datetime = str(timezone.now())
    filename = f"{folder}/{datetime}"
    data = generate_data()
    save_json(filename, data)
    # in theory, could add extra step to parse a json file to feed to this
    results = summarise(data)
    save_json(f"{filename}_summary", results)


def summarise_from_file(filename):
    data = load_json(f"{filename}.json")
    results = summarise(data)
    save_json(f"{filename}_summary", results)
