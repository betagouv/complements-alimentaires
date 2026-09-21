import json
import math
import re

from django.utils import timezone

from ai.scripts.difference_count import verify_declaration_congruence, normalise, deduplicate, diff_ingredients
import ai.scripts.prompts as prompts
from ai.mistral_pipeline import throttle

from data.models import Declaration, IngredientSynonym


CONFIGURATION = {
    "declarations_filter": {
        "article": Declaration.Article.ARTICLE_15,
        "status": Declaration.DeclarationStatus.AUTHORIZED,
        "teleicare_declaration_number__isnull": True,
        "modification_date__year": 2026,
    },
    "declarations_count": 20,
    # "dummy_extract": [
    #     [{"language": "fr", "ingredients": ["essaye"]}, {"language": "es", "ingredients": "prueba"}],
    #     [{"language": "en", "ingredients": ["test"]}, {"language": "fr", "ingredients": ["encore"]}]
    # ],
    # "dummy_clean": ["test", "clean"],
    # NB: the OCR endpoint takes no temperature, only these descriptions can
    # steer it
    "ocr": {
        "model": "mistral-ocr-4-0",
        "ingredients_description": prompts.INGREDIENTS_DESCRIPTION.format(source="file"),
        "list_type_description": prompts.LIST_TYPE_DESCRIPTION,
    },
    "pdf_text": {
        "model": "mistral-medium-latest",
        "instructions": prompts.PDF_TEXT_INSTRUCTIONS,
        "ingredients_description": prompts.INGREDIENTS_DESCRIPTION.format(source="text"),
        "list_type_description": prompts.LIST_TYPE_DESCRIPTION,
        # extraction is a deterministic task, and a high temperature has been
        # seen sending the model into inventing dozens of ingredients
        "temperature": 0.1,
    },
    "clean": {
        "model": "mistral-medium-latest",
        "instructions": prompts.CLEAN_INSTRUCTIONS,
        "temperature": 0.1,
    },
    # only called for the declarations holding a block dropped as a composition
    "match": {
        "model": "mistral-medium-latest",
        "instructions": prompts.MATCH_INSTRUCTIONS,
        "temperature": 0.1,
    },
    # a run calls the API a few times per declaration, which is enough to reach
    # the tokens per minute limit of the account: see ai/mistral_pipeline/throttle.py
    "throttle": dict(throttle.DEFAULT_THROTTLE),
}


def get_declarations(configuration):
    count = configuration["declarations_count"] or 10
    return Declaration.objects.filter(**configuration["declarations_filter"]).order_by("?")[:count]


def batch_test_declarations(configuration, data):
    data["configuration"] = configuration
    data["declarations"] = {}
    # reset first, so that a partial override given for this run does not
    # inherit the pauses of the previous one in the same shell
    throttle.reset()
    throttle.configure(**configuration.get("throttle", {}))
    configuration["throttle"] = dict(throttle.THROTTLE)
    declarations = get_declarations(configuration)
    count = 1
    data["errors"] = []
    for d in declarations:
        print("Declaration", d.id, f"(#{count})")
        try:
            data["declarations"][d.id] = verify_declaration_congruence(configuration, d)
        except Exception as e:
            print("Exception encountered")
            print(e)
            data["errors"].append(d.id)
        count += 1


# ------- Summarise data


def difference(values):
    difference = {"count": len(values)}
    if not values:
        return difference
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
    ids_no_list_found = []
    trust_threshold = 0.5
    low_trust = {"over": [], "exact": [], "under": []}
    for id, d in declarations.items():
        # when no list could be read from the labels at all, the difference is
        # the whole declared count: that is an extraction failure rather than a
        # count difference, and averaging it in hides the real accuracy
        if not d.get("list_count"):
            ids_no_list_found.append(id)
            continue
        declared_differences.append(d["declared_ingredient_count_difference"])
        total_differences.append(d["total_ingredient_count_difference"])
        if "max_difference_extracted_counts" in d and d["max_difference_extracted_counts"]:
            ids_lang_differences.append(id)
        if "list_lang" in d and d["list_lang"] != "fr":
            ids_non_french.append(id)
        if d.get("trust", 1) < trust_threshold:
            bucket = None
            diff = d["declared_ingredient_count_difference"]
            if diff < 0:
                bucket = "under"
            elif diff > 0:
                bucket = "over"
            else:
                bucket = "exact"
            low_trust[bucket].append(id)
    summary = {
        "configuration": results["configuration"],
        "declarations_count": len(declarations),
        "declared": difference(declared_differences),
        "total": difference(total_differences),
        "lang_differences": ids_lang_differences,
        "non_french_declarations": ids_non_french,
        "no_list_found": ids_no_list_found,
        "low_trust": low_trust,
        # later could add per-article, language or other groupings
    }
    return summary


# ------- Comparison file
# The raw json above holds everything but is not practical to read when
# manually checking what the AI extracted against what was declared. This
# section builds a lighter json holding, per declaration, the counts and their
# difference then both ingredient lists one after the other, sorted
# alphabetically, with the synonyms of additive codes spelled out.

# additive codes are stored as "E330" or "E160a" in data_ingredient, and their
# usual label on a product ("acide citrique") is only known as a synonym
ADDITIVE_CODE_REGEX = re.compile(r"e\d{3,4}[a-z]?")
MISSING_NAME = "(ingredient sans nom en base)"


def is_additive_code(name):
    return bool(ADDITIVE_CODE_REGEX.fullmatch(normalise(name).replace(" ", "")))


# equivalent of:
#   select name from data_ingredientsynonym
#   where standard_name_id = (select id from data_ingredient where name = <name>)
# the cache avoids repeating the same query across declarations
def get_synonyms(name, cache):
    if name not in cache:
        cache[name] = sorted(
            IngredientSynonym.objects.filter(standard_name__name__iexact=name).values_list("name", flat=True)
        )
    return cache[name]


# an additive code never appears as such on a label, so its synonyms are
# appended as a comment to give something to compare with
def format_declared_ingredient(name, synonyms_cache):
    label = name or MISSING_NAME
    synonyms = get_synonyms(name, synonyms_cache) if is_additive_code(name) else []
    if synonyms:
        label = f"{label}  # syn: {', '.join(synonyms)}"
    return label


# extracted (a) vs declared (b). The five labels overlap if taken literally
# (a=b is also within 30%, a=0 is also a<b), so they are assigned in this
# order, each declaration counted once:
#   nothing extracted → a = 0
#   perfect           → a = b
#   slight difference → b is within ±30% of a
#   over              → a > b
#   under             → a < b
SLIGHT_DIFFERENCE_RATIO = 0.30
COUNT_OUTCOMES = ("perfect", "slight difference", "over", "nothing extracted", "under")


def classify_count_outcome(extracted, declared):
    a = extracted or 0
    b = declared or 0
    if a == 0:
        return "nothing extracted"
    if a == b:
        return "perfect"
    if abs(b - a) <= SLIGHT_DIFFERENCE_RATIO * a:
        return "slight difference"
    if a > b:
        return "over"
    return "under"


# the names read from the blocks dropped as a composition, minus those the
# ingredients list already holds: only the rest is worth a call
def get_composition_candidates(results, cleaned_list):
    names = [name for composition in results.get("ignored_compositions", []) for name in composition["ingredients"]]
    already_extracted = {normalise(name) for name in cleaned_list}
    return [name for name in deduplicate(names) if normalise(name) not in already_extracted]


# keys are ordered for reading: the outcome and the counts first, then both
# ingredient lists one after the other, and finally the links to check
def build_declaration_comparison(results, synonyms_cache):
    declared_ingredients = sorted(results.get("declared_ingredients", []), key=normalise)
    cleaned_list = results.get("cleaned_list", [])
    # the names put back by the rescue pass are worth telling apart from the
    # ones read from the ingredients list itself
    rescued = results.get("rescued_from_composition", {})
    extracted_ingredients = [
        f"{name}  # composition, déclaré : {rescued[name]}" if name in rescued else name
        for name in sorted(cleaned_list, key=normalise)
    ]
    # only worth reading when the composition was mistaken for the ingredients,
    # or when dropping it left the declaration without a list
    ignored_compositions = get_composition_candidates(results, cleaned_list)
    extracted = results.get("list_count")
    declared = results.get("declared_ingredients_count")

    return {
        "outcome": classify_count_outcome(extracted, declared),
        "declared": declared,
        "extracted": extracted,
        "difference": results.get("declared_ingredient_count_difference"),
        "declared_ingredients": [format_declared_ingredient(name, synonyms_cache) for name in declared_ingredients],
        "extracted_ingredients": extracted_ingredients,
        "ignored_composition_names": sorted(ignored_compositions, key=normalise),
        # counted in total_ingredients_count, but never present on a label as such
        "computed_substances": sorted(results.get("computed_substances", []), key=normalise),
        "list_lang": results.get("list_lang"),
        "label_urls": results.get("attachments", []) + results.get("readable_pdfs", []),
        "declaration_url": results.get("declaration_url"),
        "errors": results.get("errors", []),
    }


# here, data is the higher level dict returned by batch_test_declarations
def compare(data):
    # synonyms are the same for every declaration, so they are looked up once
    synonyms_cache = {}
    counts = {label: 0 for label in COUNT_OUTCOMES}
    declarations = {}
    for declaration_id, results in data["declarations"].items():
        entry = build_declaration_comparison(results, synonyms_cache)
        counts[entry["outcome"]] += 1
        declarations[declaration_id] = entry
    # counts first, so they are what you see on opening the file
    return {
        "generated_at": timezone.now().isoformat(),
        "counts": counts,
        "declarations": declarations,
    }


# ------- main
# To run these methods:
# - ensure MEDIA_ROOT_URL is set in local env vars
# - get details of or create read only database user for db in question
# - update env vars to the remote database and read only user details
# - ensure the directory ai/scripts/results exists
# - open a shell
# - import ai.scripts.difference_count as s
# - s.run_complete() or s.summarise(<filename without extension>)
#
# run_complete writes three files, all prefixed with the run timestamp:
# - <timestamp>.json              the raw data for every declaration
# - <timestamp>_summary.json      the aggregated count differences
# - <timestamp>_comparison.json  counts by outcome first (perfect / slight
#                                 difference / over / nothing extracted / under),
#                                 then per declaration the lists side by side
#                                 for manual checking
# Both derived files can be regenerated from the raw json without calling the
# AI again, with s.summarise_from_file(...) and s.compare_from_file(...)
#
# Any key of CONFIGURATION can be overridden for one run, which is the way to
# slow the run down further when the account still answers 429:
#   s.run_complete(throttle={"min_interval": 6, "first_backoff": 60})


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename):
    data = None
    with open(f"{filename}", encoding="utf-8") as f:
        data = json.load(f)
    return data


def run_complete(return_data=False, **kwargs):
    folder = "ai/scripts/results"
    # ":" and "+" from an ISO timestamp are not valid in Windows filenames
    timestamp = timezone.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{folder}/{timestamp}"
    config = {**CONFIGURATION, **kwargs}
    data = {}
    try:
        batch_test_declarations(config, data)
    except Exception as e:
        # attempt to at least dump the data so far collected
        save_json(filename, data)
        raise e
    save_json(filename, data)
    # in theory, could add extra step to parse a json file to feed to this
    results = summarise(data)
    save_json(f"{filename}_summary", results)
    save_json(f"{filename}_comparison", compare(data))
    if return_data:
        return data


def summarise_from_file(filename):
    data = load_json(f"{filename}.json")
    results = summarise(data)
    save_json(f"{filename}_summary", results)


def compare_from_file(filename):
    data = load_json(f"{filename}.json")
    save_json(f"{filename}_comparison", compare(data))


def diff_from_file(filename):
    data = load_json(f"{filename}.json")
    if "declarations" not in data:
        print("No declarations in data")
        return
    for id, results in data["declarations"].items():
        d = Declaration.objects.get(id=id)
        diff_ingredients(results, d)
        print("only extracted", results["only_extracted"])
        print("only declared", results["only_declared"])
        print("classification", results["classification"] if "classification" in results else None)
        print("new", results["new"] if "new" in results else None)
        print("unauthorised", results["unauthorised"] if "unauthorised" in results else None)
        print("active", results["active"] if "active" in results else None)
        print("inactive", results["inactive"] if "inactive" in results else None)
        print("has_max_dose", results["has_max_dose"] if "has_max_dose" in results else None)
        print(
            "computed_substances_with_max_dose",
            results["computed_substances_with_max_dose"] if "computed_substances_with_max_dose" in results else None,
        )


def confusion_matrix():
    return {"tp": [], "fp": [], "fn": [], "tn": []}


def calculate_accuracy(tp, tn, fp, fn):
    if not tp + tn + fp + fn:
        return None
    return math.floor((tp + tn) / (tp + tn + fp + fn) * 100)


def calculate_precision(tp, tn, fp, fn):
    if not tp + fp:
        return None
    return math.floor(tp / (tp + fp) * 100)


# this method compares results against reference data
def test_data(reference_data, data):
    declaration_results = data["declarations"]
    test_results = {
        "matrices": {},
        "overall": {"good": [], "bad": []},
        "general_matrix": confusion_matrix(),
        # "declarations": {}
    }

    reference_data_iterable = reference_data.items()
    declaration_count = len(reference_data_iterable)
    for id, reference in reference_data_iterable:
        if id not in declaration_results and int(id) not in declaration_results:
            print("no result for", id)
            continue
        if "classification" not in reference:
            print("no reference classification for", id)
            continue
        result = declaration_results[id] if id in declaration_results else declaration_results[int(id)]
        classification = reference["classification"]
        if classification not in test_results["matrices"]:
            test_results["matrices"][classification] = confusion_matrix()
        default_class = "no issue detected"
        result_class = result["classification"] if "classification" in result else default_class
        if result_class not in test_results["matrices"]:
            test_results["matrices"][result_class] = confusion_matrix()

        if classification == result_class:
            test_results["matrices"][classification]["tp"].append(id)
            test_results["overall"]["good"].append(id)
            if classification == default_class:
                test_results["general_matrix"]["tn"].append(id)
        else:
            test_results["matrices"][classification]["fn"].append(id)
            test_results["matrices"][result_class]["fp"].append(id)
            test_results["overall"]["bad"].append(id)
            if classification == default_class:
                # declaration isn't being flagged as anything when it is problematic
                test_results["general_matrix"]["fn"].append(id)
            elif result_class == default_class:
                # a good declaration is being flagged as problematic
                test_results["general_matrix"]["fp"].append(id)
            else:
                # a bad declaration is being flagged for the wrong reasons
                test_results["general_matrix"]["tp"].append(id)

    for classification in test_results["matrices"]:
        tp = len(test_results["matrices"][classification]["tp"])
        fp = len(test_results["matrices"][classification]["fp"])
        fn = len(test_results["matrices"][classification]["fn"])
        tn = declaration_count - tp - fp - fn
        test_results["matrices"][classification]["accuracy"] = calculate_accuracy(tp, tn, fp, fn)
        test_results["matrices"][classification]["precision"] = calculate_precision(tp, tn, fp, fn)

    for classification, matrix in test_results["matrices"].items():
        print(classification, matrix)

    good = len(test_results["overall"]["good"])
    bad = len(test_results["overall"]["bad"])
    total = good + bad
    print("Total count : ", total)
    if total:
        print("Classification success % : ", math.floor(good / total * 100))

    tp = len(test_results["general_matrix"]["tp"])
    fp = len(test_results["general_matrix"]["fp"])
    fn = len(test_results["general_matrix"]["fn"])
    tn = len(test_results["general_matrix"]["tn"])
    print("General flag accuracy % : ", calculate_accuracy(tp, tn, fp, fn))
    print("General flag precision % : ", calculate_precision(tp, tn, fp, fn))


def test_against_file(reference_filename, data_filename):
    reference_data = load_json(f"ai/scripts/test/{reference_filename}.json")
    data = load_json(f"ai/scripts/results/{data_filename}.json")
    test_data(reference_data, data)


def run_and_test(reference_filename, **kwargs):
    reference_data = load_json(f"ai/scripts/test/{reference_filename}.json")
    ids = reference_data.keys()
    # using list here to make it serialisable when config is saved to JSON
    data = run_complete(return_data=True, declarations_filter={"id__in": list(ids)}, **kwargs)
    test_data(reference_data, data)
