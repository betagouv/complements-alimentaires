import os
import copy
from functools import lru_cache
from random import randrange
import re
from unidecode import unidecode

from data.models import Attachment, Ingredient, IngredientType
from data.choices import IngredientActivity
from data.models.ingredient_status import IngredientStatus
from ai.mistral_pipeline.ocr_extract import extract_lists, extract_lists_from_pdf
from ai.mistral_pipeline.clean_ingredients import clean_ingredient_list
from ai.mistral_pipeline.match_ingredients import match_ingredients

# ------- Misc helpers


# both lists are sorted on the normalised name, so that case, accents and
# punctuation do not scatter ingredients that read the same
def normalise(name):
    without_accents = unidecode(name or "").lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", without_accents).split())


# the declarants enter additives as their E number while labels print the usual
# name, so the comparison only works if one side is translated. The database
# already holds that mapping as ingredient synonyms.
@lru_cache(maxsize=1)
def get_additives_context():
    lines = []
    additives = Ingredient.up_to_date_objects.filter(ingredient_type=IngredientType.ADDITIVE).prefetch_related(
        "ingredientsynonym_set"
    )
    for additive in additives:
        synonyms = ", ".join(synonym.name for synonym in additive.ingredientsynonym_set.all())
        lines.append(f"{additive.name} = {synonyms}" if synonyms else additive.name)
    return "\n".join(lines)


# the same ingredient can be read twice, from two labels of one declaration or
# from the extraction and the cleaning step, which would inflate the count.
# Names are compared normalised so that case and accents do not hide a
# duplicate, and the first spelling met is the one kept.
def deduplicate(names):
    unique = {}
    for name in names:
        if not name:
            continue
        unique.setdefault(normalise(name), name)
    return list(unique.values())


# this function merges a list of dicts into one dict,
# ensuring ingredients are not lost if there are shared keys
# this also restructures the langauge lists so that the language is a key and the list a value
# the blocks read as a composition are only used as a fallback if no list is detected
def merge_lists(ingredients_lists, results=None):
    merged = {"list": {}, "composition": {}, "highlight": {}}
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
    for list_type, merged_lists in merged.items():
        for lang, value in merged_lists.items():
            merged_lists[lang] = list(set(merged_lists[lang]))
    return merged["list"] or merged["composition"] or merged["highlight"]


def save_error(results, error):
    if "errors" not in results:
        results["errors"] = []
    results["errors"].append(error)


# ------- Extract data


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

        # if couldn't find list in readable pdf, it's possible there is additional
        # non-readable text in the file, so we want to trigger OCR in this case to be sure
        found_list = False
        for list in new_lists:
            if "list_type" in list and list["list_type"] == "list":
                found_list = True
                break
        # fallback to OCR for images or non searchable PDFs
        if not found_list:
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
        if extraction and "obligatory_mentions" in extraction:
            results["obligatory_mentions"].append(extraction["obligatory_mentions"])
    return ingredients_lists


# d for declaration
def serialise_declaration_details(results, d):
    results["article"] = d.article
    results["status"] = d.status
    # NB: this URL is built from settings.HOSTNAME, so it points to the local
    # instance when the script runs locally against a remote database
    results["declaration_url"] = d.producer_url
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


# the model has been seen closing an item with leftovers of its own json, as in
# "Citrus paradisi']}". Parentheses are left alone, they belong to names such as
# "chlorure de chrome(III)".
JSON_LEFTOVERS = "'\"[]{}"


def tidy(name):
    return (name or "").strip().strip(JSON_LEFTOVERS).strip()


def clean_list(configuration, results, ingredients_list):
    if "dummy_clean" in configuration:
        return configuration["dummy_clean"]
    cleaned_list = ingredients_list
    try:
        config = configuration["clean"] if "clean" in configuration else {}
        if "instructions" in config:
            # the additives are read from the database at call time, so that
            # importing this module does not query it
            config = {**config, "instructions": f"{config['instructions']}{get_additives_context()}"}
        cleaned_list = clean_ingredient_list(ingredients_list, **config)
    except Exception as e:
        message = "Error cleaning list"
        print(message)
        save_error(results, {"message": message, "error": str(e)})
    # the cleaning step can split one item into several and reintroduce
    # duplicates that merge_lists had removed, which would inflate list_count
    cleaned_list = deduplicate(tidy(name) for name in cleaned_list)
    results["cleaned_list"] = cleaned_list
    return cleaned_list


# the model is asked for certain pairs only, but nothing stops it from answering
# with a name neither list holds, or from spending one declared ingredient on
# two candidates, which would count that ingredient twice
# def keep_certain_matches(pairs, candidates, declared):
#     candidates_by_name = {normalise(name): name for name in candidates}
#     declared_by_name = {normalise(name): name for name in declared}
#     matches = {}
#     matched_declared = set()
#     for pair in pairs:
#         if not isinstance(pair, dict):
#             continue
#         candidate = candidates_by_name.get(normalise(pair.get("candidate")))
#         reference = declared_by_name.get(normalise(pair.get("declared")))
#         if not candidate or not reference:
#             continue
#         if candidate in matches or reference in matched_declared:
#             continue
#         matches[candidate] = reference
#         matched_declared.add(reference)
#     return matches


# a block read as a composition is dropped whole, and with it the whole
# comparison when the label held nothing else. The names it held were
# ingredients after all when the producer declared them, so those that certainly
# match a declared ingredient are put back in the extracted list.
# def rescue_composition_names(configuration, results, cleaned_list):
#     candidates = get_composition_candidates(results, cleaned_list)
#     declared = results.get("declared_ingredients", [])
#     if not candidates or not declared:
#         return cleaned_list

#     matches = {}
#     try:
#         config = configuration["match"] if "match" in configuration else {}
#         pairs = match_declared_names(candidates, declared, **config)
#         matches = keep_certain_matches(pairs, candidates, declared)
#     except Exception as e:
#         message = "Error matching the composition names against the declared ingredients"
#         print(message)
#         save_error(results, {"message": message, "error": str(e)})

#     if not matches:
#         return cleaned_list
#     print(f"Rescued {len(matches)} name(s) from a composition")
#     results["rescued_from_composition"] = matches
#     # the rescued names keep the spelling read from the label, as the rest of
#     # the extracted list does
#     cleaned_list = deduplicate(cleaned_list + list(matches.keys()))
#     results["cleaned_list"] = cleaned_list
#     return cleaned_list


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


# ------- match and diff ingredients


def check_article(results, ingredient_names, matches):
    possible_missing_ingredients = []
    new = []
    for name in ingredient_names:
        possible_missing_ingredients += matches[name]
        if not matches[name]:
            new.append(name)
    unauthorised = []
    active = []
    inactive = []
    has_max_dose = []
    computed_substances_with_max_dose = []

    for ingredient in possible_missing_ingredients:
        # TODO: add authorization revoked? not currently in use though
        if ingredient.status == IngredientStatus.NOT_AUTHORIZED:
            unauthorised.append(ingredient)
        if ingredient.activity == IngredientActivity.ACTIVE:
            active.append(ingredient)
        else:
            inactive.append(ingredient)
        if ingredient.max_quantities.exists():
            has_max_dose.append(ingredient)
        if ingredient.object_type != "substance" and ingredient.substances.exists():
            computed_substances_with_max_dose += ingredient.substances.exclude(max_quantities=None)[::1]

    classification = None
    if new:
        classification = "missing new"
    elif unauthorised:
        classification = "missing unauthorised"
    elif has_max_dose or computed_substances_with_max_dose:
        classification = "max dose risk"
    elif active:
        classification = "missing active"
    elif inactive:
        classification = "missing inactive"

    results["classification"] = classification
    results["new"] = new
    results["unauthorised"] = [name_with_type(i) for i in unauthorised]
    results["active"] = [name_with_type(i) for i in active]
    results["inactive"] = [name_with_type(i) for i in inactive]
    results["has_max_dose"] = [name_with_type(i) for i in has_max_dose]
    results["computed_substances_with_max_dose"] = [name_with_type(i) for i in computed_substances_with_max_dose]


def name_with_type(obj):
    return f"{obj.name} [{obj.object_type_fr}]"


def diff_ingredients(results, d):
    declared_ingredients = []
    ing_types = ["ingredient", "plant", "microorganism", "substance"]
    for type in ing_types:
        qs = getattr(d, f"declared_{type}s")
        for declared_ing in qs.all():
            declared_ingredients.append(getattr(declared_ing, type))

    extracted_ingredients = results.get("cleaned_list", [])
    matches = match_ingredients(extracted_ingredients)
    serialized_matches = {}
    for name, suggestions in matches.items():
        serialized_matches[name] = [name_with_type(i) for i in suggestions]
    results["matches"] = serialized_matches
    only_declared = []
    matched_ingredients = []
    matched_extracted_ingredients = []
    # TODO: how will this logic work with plant parts and preparations in account?
    for d_ing in declared_ingredients:
        has_match = False
        for extracted_ingredient, suggestions in matches.items():
            # avoid accidentally matching one declared ingredient to two or more extracted
            # TODO: what about ingredients declared more than once?
            if extracted_ingredient not in matched_extracted_ingredients:
                if d_ing in suggestions:
                    # we have a declared ingredient that is also extracted
                    matched_ingredients.append((d_ing, extracted_ingredient))
                    has_match = True
                    matched_extracted_ingredients.append(extracted_ingredient)
                    break
        if not has_match:
            only_declared.append(d_ing)
    all_extracted = matches.keys()
    only_extracted = set(all_extracted) - set(matched_extracted_ingredients)

    only_extracted = list(only_extracted) if only_extracted else []
    if only_extracted:
        check_article(results, only_extracted, matches)

    results["only_extracted"] = only_extracted
    results["only_declared"] = [name_with_type(i) for i in only_declared]


def verify_declaration_congruence(configuration, declaration):
    declaration_results = {}
    serialise_declaration_details(declaration_results, declaration)

    # get all ingredients present in the attachments
    ingredients_lists = extract_ingredients(configuration, declaration_results, declaration)
    declaration_results["extracted_ingredients"] = ingredients_lists
    merged_ingredients_lists = merge_lists(ingredients_lists, declaration_results)
    save_extracted_lists_stats(declaration_results, merged_ingredients_lists)

    # choose the ingredients list we will use for comparison with the declared
    chosen_list = pick_list(declaration_results, merged_ingredients_lists)
    cleaned_list = clean_list(configuration, declaration_results, chosen_list)
    declaration_results["list_count"] = len(cleaned_list)
    save_differential(declaration_results)
    calculate_trust_score(declaration_results)

    # identify the difference between declared and extracted ingredients
    diff_ingredients(declaration_results, declaration)
    return declaration_results
