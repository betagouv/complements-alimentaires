import os
import json
import math
import copy
import re
from functools import lru_cache
from random import randrange

from django.utils import timezone

from unidecode import unidecode

from data.models import Declaration, Attachment, Ingredient, IngredientSynonym, IngredientType
from ai.mistral_pipeline.ocr_extract import extract_lists, extract_lists_from_pdf
from ai.mistral_pipeline.clean_ingredients import clean_ingredient_list
from ai.mistral_pipeline.match_declared import match_declared_names
from ai.mistral_pipeline import throttle

# ------- Prompts
# These are written from the differences observed between the declared and the
# extracted lists. Each rule below fixes a mistake seen in a previous run, and
# is kept here rather than in the pipeline so that a run can override it.

# The declared side of the comparison holds one row per ingredient, so the
# extracted side must too. The main source of undercounting was the model
# returning a single item for a whole functional category or premix, and the
# main source of overcounting the composition being read as ingredients.
INGREDIENTS_DESCRIPTION = """a list of the ingredient names of the food supplement, with exactly one ingredient per array item.

Return the ingredients the product is made of, and not its composition. A label most often prints both, and their headings are unreliable, so tell them apart by their shape rather than by the words they use:
- the ingredients are given as running text, names separated by commas, in decreasing order of weight, holding the excipients and the additives next to the active ingredients.
- the composition is a table, or a series of lines, giving what a daily dose provides, where every name carries a quantity, a unit or a percentage of reference intake ("VNR", "AR", "%").
A name is therefore not an ingredient because of what it is, but because of where it is written: read a name as an ingredient when it appears among the ingredients, and ignore the same name when it only appears in the composition.
When one block holds both, an ingredients text followed or interrupted by quantified lines, return only the names belonging to its ingredients part.

An ingredient and what it provides are frequently written together, in which case return the ingredient alone:
- "vitamine C (acide L-ascorbique)" and "acide L-ascorbique (vitamine C)" both give "acide L-ascorbique", the form the product is made with.
- "zinc (citrate de zinc)" gives "citrate de zinc"; "magnésium (oxyde de magnésium)" gives "oxyde de magnésium".
- "huile de poisson (EPA, DHA)" gives "huile de poisson": EPA and DHA are what the oil provides, not other ingredients.
The nutrient name is itself the ingredient when the ingredients give no other form for it: "Ingrédients : vitamine C, zinc, gomme d'acacia" gives "vitamine C", "zinc" then "gomme d'acacia".

Split anything holding several ingredients into separate items:
- functional categories, dropping the category name: "acidifiants : acide citrique, citrate de sodium" gives "acide citrique" then "citrate de sodium"; "agents d'enrobage : huile de coco, cire de carnauba" gives "huile de coco" then "cire de carnauba". Never return the category on its own, as in "agent de charge", "anti-agglomérant" or "agent d'enrobage".
- premixes and parentheses listing several ingredients: "prémélange d'ingrédients actifs (acétate de rétinyle, iodure de potassium)" gives "acétate de rétinyle" then "iodure de potassium".
Keep the following intact:
- for an additive, keep its E number in the same item as its name when both are written, as in "acide citrique (E330)". Return the E number alone when the name is not given.
- for a plant, return the botanical binomial name when it appears anywhere in the item, dropping the preparation and the part used: "extrait de racine de maca (Lepidium meyenii)" gives "Lepidium meyenii". Without a binomial name, drop the part used only: "matricaire capitule" gives "matricaire".
Never return an ingredient that is not literally written in the {source}, never complete a list from your own knowledge, and never return the same ingredient twice.
Do not return allergen warnings ("contient : lait"), nutritional values, quantities, percentages, claims or usage advice.
Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that."""

# "'list' or 'composition'" alone left the model guessing, and a list wrongly
# labelled "composition" is dropped by merge_lists
LIST_TYPE_DESCRIPTION = """'list' when the names you return come from the ingredients of the product: running text, names separated by commas, in decreasing order of weight, usually introduced by "Ingrédients :", "Ingredients:" or an equivalent, and holding the additives and the excipients.
'composition' when they come from a table of nutritional values or of active substances per daily dose, where each line carries a quantity, a unit or a percentage of reference intake.
Decide on the shape of the block and not on its heading: running text separated by commas under a heading reading "composition" is still a 'list', and a quantified table under a heading reading "ingrédients" is still a 'composition'.
When a block holds both, answer 'list' and return only the names from its ingredients part.
Only when neither shape can be recognised, answer 'list'."""

PDF_TEXT_INSTRUCTIONS = """The user will send you the text extracted from a PDF label of a food supplement ("complément alimentaire") sold in France. Respond with the ingredients lists present in the text.
The same list is often printed in several languages: return one entry per language and never merge two languages into one entry. The language you report is the one the ingredient names themselves are written in, not the language of the rest of the packaging."""

# A block read as a composition is dropped whole by merge_lists, and runs show
# that the real ingredients list is sometimes the block dropped, leaving nothing
# to compare against the declaration. A name the producer declared was an
# ingredient after all, so this pass looks for the dropped names that are
# certainly declared ones. Certainty is what makes the pass safe: a pair is only
# accepted for two spellings of one ingredient, never for two related ones,
# which keeps the composition of a product whose actives are declared from being
# counted as its ingredients.
MATCH_INSTRUCTIONS = """You are given two lists of ingredient names of the same food supplement, 'candidates' read from one block of its label and 'declared' taken from the declaration filed by its producer.
Return an object with a key 'matches' holding an array of objects with the keys 'candidate' and 'declared', pairing a candidate with the declared name that designates the same ingredient.

Only return a pair when the two names designate one and the same ingredient beyond doubt, which is the case when they differ only by:
- spelling, case, accents, hyphenation, plural or word order, including an obvious misreading of the label: "Résveratrol" and "resvératrol", "zinc picolinate" and "Picolinate de zinc", "méthylcobalamin" and "Méthylcobalamine".
- the language they are written in: "whey protein concentrate" and "Protéine de petit-lait", "Turmeric" and "curcuma".
- a preparation, a plant part, a form or a grade left out on one side: "extrait sec de racine (Rhodiola rosea)" and "Rhodiola rosea", "poudre de shiitaké" and "Lentinula edodes".
- the botanical name against another accepted botanical name of the same species, or against its vernacular name: "Rhodiola rosea" and "Sedum roseum (L.) Scop.".
- the name of an additive against its E number: "gomme d'acacia" and "E414".

Return no pair when the two names are only related, and in particular never pair:
- a nutrient with the form that supplies it: "Vitamine C" is not "Acide L-ascorbique", "Vitamine E" is not "Acétate de D-alpha-tocophéryle", "magnésium" is not "Oxyde de magnésium".
- a substance with the ingredient it is drawn from: "Turmeric Extract" is not "curcuminoïdes", "huile de poisson" is not "acide eicosapentaénoïque".
- two forms of the same nutrient, two salts of the same mineral, or two species of the same genus: "citrate de magnésium" is not "Oxyde de magnésium", "Lactobacillus casei" is not "Lactobacillus acidophilus".

Pair each candidate with at most one declared name and each declared name with at most one candidate. Leave out every candidate you cannot pair with certainty, and never return a name that is absent from the list it is given for."""

# The additives table read from the database is appended to these instructions,
# see get_additives_context
CLEAN_INSTRUCTIONS = """You are given a list of raw ingredient strings read from the label of a food supplement. Return an object with a key 'ingredients' holding an array of ingredient names, with exactly one ingredient per item and no duplicates.
- split any item still holding several ingredients, dropping the functional category: "acidifiants : acide citrique, citrate de sodium" gives "acide citrique" then "citrate de sodium".
- replace an additive by its E number using the table below, whether the input gives the name, the E number, or both. Leave alone an item the label uses as a vitamin or mineral source rather than as an additive, such as "acide L-ascorbique", "carbonate de calcium" or "lactate de calcium", even when the table holds an E number for it.
- for a plant, return only the botanical binomial name where one is given, dropping the preparation and the part used.
- remove quantities, percentages, allergen mentions and claims.
- drop an item naming only what another item of the input provides, keeping the form the product is made with: "vitamine C" next to "acide L-ascorbique" gives "acide L-ascorbique" alone, "vitamine B12" next to "cyanocobalamine" gives "cyanocobalamine" alone, and "EPA" and "DHA" next to "huile de poisson" give "huile de poisson" alone. Keep a nutrient name that no other item accounts for.
- drop an item that names a functional category only, as in "agent de charge", "anti-agglomérant" or "agent d'enrobage".
- never add an ingredient absent from the input, and never drop one for any other reason than the two rules above.

# Additives, as "E number = usual names"
"""

# ------- Misc helpers

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
        "ingredients_description": INGREDIENTS_DESCRIPTION.format(source="file"),
        "list_type_description": LIST_TYPE_DESCRIPTION,
    },
    "pdf_text": {
        "model": "mistral-medium-latest",
        "instructions": PDF_TEXT_INSTRUCTIONS,
        "ingredients_description": INGREDIENTS_DESCRIPTION.format(source="text"),
        "list_type_description": LIST_TYPE_DESCRIPTION,
        # extraction is a deterministic task, and a high temperature has been
        # seen sending the model into inventing dozens of ingredients
        "temperature": 0.1,
    },
    "clean": {
        "model": "mistral-medium-latest",
        "instructions": CLEAN_INSTRUCTIONS,
        "temperature": 0.1,
    },
    # only called for the declarations holding a block dropped as a composition
    "match": {
        "model": "mistral-medium-latest",
        "instructions": MATCH_INSTRUCTIONS,
        "temperature": 0.1,
    },
    # a run calls the API a few times per declaration, which is enough to reach
    # the tokens per minute limit of the account: see ai/mistral_pipeline/throttle.py
    "throttle": dict(throttle.DEFAULT_THROTTLE),
}


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


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename):
    data = None
    with open(f"{filename}", encoding="utf-8") as f:
        data = json.load(f)
    return data


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
# the blocks read as a composition are dropped, but kept in the results, both
# to explain a declaration ending up with no list at all and to feed
# rescue_composition_names
def merge_lists(ingredients_lists, results=None):
    merged_lists = {}
    for extraction in ingredients_lists:
        for language_result in extraction:
            # TODO: handle potentially malformatted responses?
            lang = language_result["language"]
            value = language_result["ingredients"]
            list_type = language_result["list_type"]
            if list_type == "composition":
                if results is not None:
                    results.setdefault("ignored_compositions", []).append(language_result)
                continue
            if lang not in merged_lists:
                merged_lists[lang] = copy.deepcopy(value)
            else:
                merged_lists[lang] += value
    for lang, value in merged_lists.items():
        merged_lists[lang] = deduplicate(value)
    return merged_lists


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
        if extraction and "obligatory_mentions" in extraction:
            results["obligatory_mentions"].append(extraction["obligatory_mentions"])
    return ingredients_lists


# d for declaration
def save_declaration_details(results, d):
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


# ------- Rescue the names dropped with a composition


# the names read from the blocks dropped as a composition, minus those the
# ingredients list already holds: only the rest is worth a call
def get_composition_candidates(results, cleaned_list):
    names = [name for composition in results.get("ignored_compositions", []) for name in composition["ingredients"]]
    already_extracted = {normalise(name) for name in cleaned_list}
    return [name for name in deduplicate(names) if normalise(name) not in already_extracted]


# the model is asked for certain pairs only, but nothing stops it from answering
# with a name neither list holds, or from spending one declared ingredient on
# two candidates, which would count that ingredient twice
def keep_certain_matches(pairs, candidates, declared):
    candidates_by_name = {normalise(name): name for name in candidates}
    declared_by_name = {normalise(name): name for name in declared}
    matches = {}
    matched_declared = set()
    for pair in pairs:
        if not isinstance(pair, dict):
            continue
        candidate = candidates_by_name.get(normalise(pair.get("candidate")))
        reference = declared_by_name.get(normalise(pair.get("declared")))
        if not candidate or not reference:
            continue
        if candidate in matches or reference in matched_declared:
            continue
        matches[candidate] = reference
        matched_declared.add(reference)
    return matches


# a block read as a composition is dropped whole, and with it the whole
# comparison when the label held nothing else. The names it held were
# ingredients after all when the producer declared them, so those that certainly
# match a declared ingredient are put back in the extracted list.
def rescue_composition_names(configuration, results, cleaned_list):
    candidates = get_composition_candidates(results, cleaned_list)
    declared = results.get("declared_ingredients", [])
    if not candidates or not declared:
        return cleaned_list

    matches = {}
    try:
        config = configuration["match"] if "match" in configuration else {}
        pairs = match_declared_names(candidates, declared, **config)
        matches = keep_certain_matches(pairs, candidates, declared)
    except Exception as e:
        message = "Error matching the composition names against the declared ingredients"
        print(message)
        save_error(results, {"message": message, "error": str(e)})

    if not matches:
        return cleaned_list
    print(f"Rescued {len(matches)} name(s) from a composition")
    results["rescued_from_composition"] = matches
    # the rescued names keep the spelling read from the label, as the rest of
    # the extracted list does
    cleaned_list = deduplicate(cleaned_list + list(matches.keys()))
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


def generate_data(configuration, data):
    data["configuration"] = configuration
    data["declarations"] = {}
    # reset first, so that a partial override given for this run does not
    # inherit the pauses of the previous one in the same shell
    throttle.reset()
    throttle.configure(**configuration.get("throttle", {}))
    configuration["throttle"] = dict(throttle.THROTTLE)
    declarations = get_declarations(configuration)
    count = 1
    for d in declarations:
        print("Declaration", d.id, f"(#{count})")
        declaration_results = {}
        save_declaration_details(declaration_results, d)

        # get all ingredients present in the attachments
        ingredients_lists = extract_ingredients(configuration, declaration_results, d)
        declaration_results["extracted_ingredients"] = ingredients_lists
        merged_ingredients_lists = merge_lists(ingredients_lists, declaration_results)
        save_extracted_lists_stats(declaration_results, merged_ingredients_lists)

        # choose the ingredients list we will use for comparison with the declared
        chosen_list = pick_list(declaration_results, merged_ingredients_lists)
        cleaned_list = clean_list(configuration, declaration_results, chosen_list)
        cleaned_list = rescue_composition_names(configuration, declaration_results, cleaned_list)
        declaration_results["list_count"] = len(cleaned_list)
        save_differential(declaration_results)
        calculate_trust_score(declaration_results)

        # finally, save the results
        data["declarations"][d.id] = declaration_results
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


# both lists are sorted on the normalised name, so that case, accents and
# punctuation do not scatter ingredients that read the same
def normalise(name):
    without_accents = unidecode(name or "").lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", without_accents).split())


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


# here, data is the higher level dict returned by generate_data
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


def run_complete(**kwargs):
    folder = "ai/scripts/results"
    # ":" and "+" from an ISO timestamp are not valid in Windows filenames
    timestamp = timezone.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{folder}/{timestamp}"
    config = {**CONFIGURATION, **kwargs}
    data = {}
    try:
        generate_data(config, data)
    except Exception as e:
        # attempt to at least dump the data so far collected
        save_json(filename, data)
        raise e
    save_json(filename, data)
    # in theory, could add extra step to parse a json file to feed to this
    results = summarise(data)
    save_json(f"{filename}_summary", results)
    save_json(f"{filename}_comparison", compare(data))


def summarise_from_file(filename):
    data = load_json(f"{filename}.json")
    results = summarise(data)
    save_json(f"{filename}_summary", results)


def compare_from_file(filename):
    data = load_json(f"{filename}.json")
    save_json(f"{filename}_comparison", compare(data))
