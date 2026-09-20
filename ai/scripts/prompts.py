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

For an additive, keep its E number in the same item as its name when both are written, as in "acide citrique (E330)". Return the E number alone when the name is not given.

Where the botanical binomial name of a plant appears anywhere in the item return only this name, dropping the preparation and the part used: "extrait de racine de maca (Lepidium meyenii)" gives "Lepidium meyenii" and "huile de tournesol (Helianthus annuus)" gives "Helianthus annuus". Without a binomial name, drop the part used only: "matricaire capitule" gives "matricaire".

Never return an ingredient that is not literally written in the {source}, never complete a list from your own knowledge, and never return the same ingredient twice.
Do not return allergen warnings ("contient : lait"), nutritional values, quantities, percentages, claims or usage advice.
Some products only contain one ingredient, where a list of ingredients is not present, check whether the title contains the name of the ingredient and return that."""

# "'list' or 'composition'" alone left the model guessing, and a list wrongly
LIST_TYPE_DESCRIPTION = """'list' when the names you return come from the ingredients of the product: running text, names separated by commas, in decreasing order of weight, usually introduced by "Ingrédients :", "Ingredients:" or an equivalent, and holding the additives and the excipients.
'composition' when they come from a table of nutritional values or of active substances per daily dose, where each line carries a quantity, a unit or a percentage of reference intake.
'highlight' when ingredient names are listed near the product title, often in bullet point and larger font, not introduced by a term such as 'Ingrédients :'.
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
