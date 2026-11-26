"""Strict Pydantic schemas: model outputs and the pipeline's business objects.

Every fact read on the label carries its proof (verbatim quote + page). A quote that cannot be
found again in the OCR transcript is flagged "not grounded" and can never justify a block on
its own (see extract.grounded and decision.is_blocking).

IMPORTANT: the `Field(description=...)` texts below are sent to the model as part of the JSON
schema (llm.client.strict_schema). They are prompt text, written in French like the labels and
the prompts/ folder, and changing them changes the model's behaviour and invalidates the cache.
For the same reason the models below have no class docstrings (Pydantic would put them in the
schema too): explanations for developers are `#` comments.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

# Bump when a schema changes in a way that must invalidate cached extractions.
SCHEMA_VERSION = "2.0"


# ============================================================================ extraction (vision model output)
class DocumentKind(str, Enum):
    packaging_artwork = "packaging_artwork"  # packaging artwork / print proof
    label_photo = "label_photo"  # photo of a real product
    text_document = "text_document"  # text document (Word, spreadsheet...) that is not a label
    form_screenshot = "form_screenshot"  # screenshot of the Compl'Alim form or of a website
    technical_sheet = "technical_sheet"  # technical sheet / certificate / lab analysis
    other = "other"


class Legibility(str, Enum):
    good = "good"
    partial = "partial"
    poor = "poor"


class MentionStatus(str, Enum):
    present = "present"
    absent = "absent"
    unclear = "unclear"


# Basis of a quantity written on the label. Only per_daily_dose can be compared directly with the
# declaration; per_unit is multiplied by the number of units per day (rules.label_quantities).
class Basis(str, Enum):
    per_daily_dose = "per_daily_dose"
    per_unit = "per_unit"  # per capsule / tablet / ml / drop
    per_100 = "per_100"  # per 100 g / 100 ml
    per_serving = "per_serving"  # per serving (when different from the daily dose)
    unknown = "unknown"


# A verbatim quote from the label and the page it is on (0-based).
class Evidence(BaseModel):
    quote: str = Field(description="Citation EXACTE, recopiée mot pour mot depuis l'étiquette")
    page: int = Field(description="Numéro de page (0 = première page)")


# Standardised content of an extract, e.g. "titrated to 95 % curcuminoids".
class Standardisation(BaseModel):
    substance: str = Field(description="Substance titrée, ex. 'curcuminoïdes', 'rosavines'")
    percent: float | None = Field(description="Titrage en %, ex. 95 pour 'titré à 95 %'")
    quantity: float | None = Field(description="Quantité de la substance si écrite")
    unit: str | None


# One entry of the label's ingredient list, decomposed so that entity resolution can match the
# species (plant), the part and the preparation separately.
class LabelIngredient(BaseModel):
    raw: str = Field(description="Libellé tel qu'écrit, verbatim")
    name: str = Field(description="Nom de l'ingrédient seul (sans partie, préparation ni quantité)")
    botanical_name: str | None = Field(description="Nom latin binomial si écrit (ex. 'Rhodiola rosea')")
    plant_part: str | None = Field(description="Partie de plante si écrite (racine, feuille, fruit…)")
    preparation: str | None = Field(
        description="Préparation si écrite (extrait sec, poudre, huile essentielle, teinture…)"
    )
    extract_ratio: str | None = Field(description="Ratio d'extraction si écrit, ex. '4:1'")
    standardisation: list[Standardisation]
    e_number: str | None = Field(description="Code E si écrit, ex. 'E464'")
    functional_class: str | None = Field(
        description="Catégorie fonctionnelle si écrite (agent de charge, anti-agglomérant, enveloppe…)"
    )
    is_capsule_shell: bool = Field(description="Vrai si c'est l'enveloppe de la gélule/capsule")
    is_active: bool = Field(
        description="Vrai si ingrédient actif (plante, nutriment, substance à effet), faux si excipient/additif/arôme"
    )
    quantity: float | None = Field(description="Quantité écrite à côté de l'ingrédient, si présente")
    unit: str | None
    basis: Basis
    percentage: float | None = Field(description="Pourcentage dans le produit si écrit")
    from_premix: str | None = Field(description="Nom du prémélange/mélange parent si l'ingrédient en fait partie")
    page: int


# One row of a composition / nutrition table ("Zinc 10 mg (100 % NRV)").
class CompositionRow(BaseModel):
    raw: str = Field(description="Ligne telle qu'écrite, verbatim")
    name: str = Field(description="Nutriment / substance / ingrédient de la ligne")
    value: float | None
    unit: str | None = Field(description="mg, µg, g, UI, UFC, ml…")
    basis: Basis
    basis_text: str | None = Field(description="Ex. 'pour 2 gélules', 'par DJR (3 comprimés)'")
    nrv_percent: float | None = Field(description="% VNR/AR si indiqué")
    is_sub_row: bool = Field(
        description="Vrai pour une ligne 'dont …' (substance contenue dans l'ingrédient au-dessus)"
    )
    parent: str | None = Field(description="Ingrédient parent pour une ligne 'dont …'")
    page: int


class Mention(BaseModel):
    status: MentionStatus
    quote: str | None = Field(description="Citation exacte si présente")
    page: int | None


# Mandatory statements of decree 2006-352 (art. 10 and 12) and of the INCO regulation 1169/2011.
# Checked by rules.rule_mentions, which never trusts an "absent" without a text double-check.
class Mentions(BaseModel):
    denomination_complement_alimentaire: Mention = Field(description="La dénomination 'complément alimentaire'")
    nutrient_categories: Mention = Field(
        description="Les catégories de nutriments/substances caractérisant le produit"
    )
    daily_dose: Mention = Field(description="La portion journalière recommandée (ex. '2 gélules par jour')")
    warning_do_not_exceed: Mention = Field(
        description="Avertissement : ne pas dépasser la dose journalière recommandée"
    )
    warning_varied_diet: Mention = Field(
        description="Déclaration : ne pas utiliser comme substitut d'un régime alimentaire varié"
    )
    warning_children: Mention = Field(description="Tenir hors de la portée des jeunes enfants")
    quantities_per_daily_dose: Mention = Field(
        description="Quantités des actifs rapportées à la DJR, sous forme numérique"
    )
    ingredients_list: Mention = Field(description="Liste des ingrédients (introduite par 'Ingrédients')")
    net_quantity: Mention = Field(description="Quantité nette (g, ml, nombre d'unités + poids)")
    best_before: Mention = Field(
        description="Date de durabilité minimale ou emplacement prévu ('à consommer de préférence avant…')"
    )
    lot: Mention = Field(description="Numéro de lot ou emplacement prévu")
    operator: Mention = Field(description="Nom/raison sociale et adresse de l'exploitant")


class ProductIdentity(BaseModel):
    name: str | None
    brand: str | None
    galenic_form: str | None = Field(description="gélule, comprimé, poudre, liquide, gouttes…")
    net_quantity: str | None
    unit_count: float | None = Field(description="Nombre d'unités dans le conditionnement, si écrit")


class DailyDose(BaseModel):
    text: str | None = Field(description="Texte exact de la posologie")
    units_per_day_max: float | None = Field(
        description="Nombre MAXIMAL d'unités par jour (ex. 3 pour '2 à 3 gélules')"
    )
    unit_kind: str | None = Field(description="gélule, comprimé, ml, gouttes, g, sachet, ampoule…")
    page: int | None


# Everything the vision model extracts from ONE label file. It is produced "blind": the model
# never sees the declaration, so it cannot be biased towards confirming it (extract.py).
class LabelExtraction(BaseModel):
    is_food_supplement_label: bool = Field(
        description="Le document est-il une étiquette/emballage de complément alimentaire ?"
    )
    document_kind: DocumentKind
    legibility: Legibility
    languages: list[str] = Field(description="Langues présentes (ISO 639-1)")
    french_present: bool
    product: ProductIdentity
    daily_dose: DailyDose
    ingredients: list[LabelIngredient] = Field(
        description="Liste des ingrédients en français, UN par élément, dans l'ordre"
    )
    composition: list[CompositionRow] = Field(description="Tableau/lignes de composition avec quantités")
    mentions: Mentions
    warnings: list[Evidence] = Field(description="TOUS les avertissements, précautions, contre-indications, verbatim")
    claims: list[Evidence] = Field(description="Allégations et promesses (santé, effets), verbatim")
    target_populations: list[str] = Field(
        description="Populations visées explicitement (enfants, femmes enceintes, sportifs…)"
    )
    anomalies: list[str] = Field(
        description="Signes de faux : texte de remplissage, 'XXX', 'lorem', champs vides, autre produit…"
    )


# ============================================================================ entity resolution
# Output of the small resolution model: for each label item, one uid picked AMONG that item's
# candidates, or "NONE". resolve.Resolver rejects any uid that was not offered as a candidate.
class ResolveChoice(BaseModel):
    index: int = Field(description="Index de l'item dans la liste reçue")
    uid: str = Field(
        description="uid choisi parmi les candidats de CET item, ou 'NONE' si aucun ne désigne le même ingrédient"
    )
    confidence: float = Field(description="Confiance entre 0 et 1")
    reason: str


class ResolveBatch(BaseModel):
    choices: list[ResolveChoice]


# Final resolution of one label row (whatever the method), as used by the rules.
class Resolution(BaseModel):
    text: str
    uid: str | None = None
    confidence: float = 0.0
    method: str = "none"  # alias | e_number | botanical | exact | exact_context | llm | none
    part_id: int | None = None  # resolved plant part (plants only)
    candidates: list[str] = Field(default_factory=list)
    reason: str = ""


# ============================================================================ findings / decision
# BLOCKING: can block on its own once proven. MAJOR: blocks only if confirmed by the agent AND listed
# in the policy (config.confirmed_major_codes). MINOR / INFO: only feed the risk score.
class Severity(str, Enum):
    BLOCKING = "BLOCKING"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    INFO = "INFO"


# The fraud types the pipeline targets (see the README for the mapping to rules).
class FraudType(str, Enum):
    fake_label = "fake_label"
    undeclared_ingredients = "undeclared_ingredients"
    article_bypass = "article_bypass"
    dose_underdeclared = "dose_underdeclared"
    label_noncompliance = "label_noncompliance"


# One finding raised by a rule. `title` and `detail` are written in French because they end up in
# the message sent to the declarant (decision.build_message).
class Finding(BaseModel):
    id: str
    code: str  # rule code, e.g. "R-ART-BYPASS" (prefix = rule family)
    severity: Severity
    fraud_type: FraudType
    confidence: float
    title: str
    detail: str
    evidence: list[Evidence] = Field(default_factory=list)
    grounded: bool = True  # every quote was found again in the label text
    refs: list[str] = Field(default_factory=list)  # uids of the elements involved
    verified: str | None = None  # confirmed | refuted | uncertain (set by the agent)
    verification_note: str | None = None


class Decision(BaseModel):
    decision: str  # BLOCK | PASS | ERROR (ERROR = technical failure, to be replayed, never a block)
    risk_score: float
    blocking_findings: list[str]
    reason_codes: list[str]
    message_to_declarant: str
    counterfactual_article: str | None = None
    declared_article: str | None = None


# Agent output, collected from its final `rendre_verdict` tool call (agent.VerificationAgent).
class AgentVerdict(BaseModel):
    finding_id: str
    verdict: str = Field(description="confirmed | refuted | uncertain")
    confidence: float
    quote: str | None
    page: int | None
    explanation: str


class AgentOutput(BaseModel):
    verdicts: list[AgentVerdict]
    new_findings: list[str] = Field(
        description="Problèmes supplémentaires constatés, une phrase chacun (peut être vide)"
    )


# Output of the warning check (rules.rule_specific_warnings): one status per required warning.
class WarningCheckItem(BaseModel):
    index: int
    status: str = Field(description="present | absent | partial")
    quote: str | None
    page: int | None


class WarningCheck(BaseModel):
    items: list[WarningCheckItem]
