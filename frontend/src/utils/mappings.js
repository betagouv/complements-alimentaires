export const getTypeIcon = (type) => {
  const iconMapping = {
    plant: "ri-plant-line",
    plant_part: "ri-seedling-line",
    microorganism: "ri-microscope-line",
    form_of_supply: "ri-contrast-drop-line",
    aroma: "ri-bubble-chart-line",
    additive: "ri-filter-2-line",
    active_ingredient: "ri-flask-line",
    non_active_ingredient: "ri-flask-line",
    substance: "ri-test-tube-line",
  }
  return iconMapping[type] || "ri-drop-line"
}

export const typesMapping = {
  plant: "Plante",
  plant_part: { singular: "Partie de plante", plural: "Parties de plante" },
  microorganism: "Micro-organisme",
  form_of_supply: "Forme d'apport", // nutrient: "Nutriment"
  aroma: "Arôme",
  additive: "Additif",
  active_ingredient: "Autre ingredient actif",
  non_active_ingredient: "Autre ingredient non actif", // TODO : merger ces 2 types en 1 et n'utiliser que le label "actif"/"inactif"
  substance: "Substance",
  // TODO: déprecier après l'import de données extraites en mai 2024
  // qui contient les types plus précis
  ingredient: "Autre ingrédient",
}
export const frontToAPITypesSlugMapping = {
  plante: "plant",
  "micro-organisme": "microorganism",
  "forme-d-apport": "form_of_supply",
  arôme: "aroma",
  additif: "additive",
  "ingredient-actif": "active_ingredient",
  "ingredient-non-actif": "non_active_ingredient",
  substance: "substance",
  // déprécié
  "autre-ingredient": "ingredient",
  ingredient: "ingredient",
}
export const getTypeInFrench = (type) => {
  return typesMapping[type] || null
}

export const slugifyType = (type) => {
  return Object.keys(frontToAPITypesSlugMapping).find(
    (key) => frontToAPITypesSlugMapping[key].toLowerCase() === type.toLowerCase()
  )
}

export const unSlugifyType = (typeSlug) => {
  return frontToAPITypesSlugMapping[typeSlug] || null
}

export const getApiType = (type) => {
  switch (type) {
    case "form_of_supply":
    case "aroma":
    case "additive":
    case "active_ingredient":
    case "non_active_ingredient":
    case "ingredient":
      return "other-ingredient"
    default:
      return `${type.replace("_", "-")}`
  }
}

export const getActivityReadonlyByType = (type) => {
  switch (type) {
    case "plant":
      return false
    default:
      return true
  }
}

/* Cette fonction n'est utile que pour les ingrédients nouveaux, créés lors de la déclaration
Pour tous les autres, l'activitée est fournie par le backend */
export const getActivityByType = (type) => {
  switch (type) {
    case "plant":
    case "microorganism":
    case "active_ingredient":
    case "form_of_supply":
    case "substance":
    case "ingredient":
      return true
    default:
      return false
  }
}

export const statusProps = {
  DRAFT: {
    icon: "ri-pencil-fill",
    label: "Brouillon",
  },
  INSTRUCTION: {
    icon: "ri-time-fill",
    label: "Instruction",
  },
  AWAITING_INSTRUCTION: {
    icon: "ri-time-fill",
    label: "En attente d'instruction",
  },
  ONGOING_INSTRUCTION: {
    icon: "ri-todo-fill",
    label: "En cours d'instruction",
  },
  AWAITING_VISA: {
    icon: "ri-time-fill",
    label: "En attente de visa / signature",
  },
  ONGOING_VISA: {
    icon: "ri-todo-fill",
    label: "En cours de visa / signature",
  },
  OBJECTION: {
    icon: "ri-error-warning-line",
    label: "Objection",
  },
  OBSERVATION: {
    icon: "ri-file-search-fill",
    label: "Observation",
  },
  ABANDONED: {
    icon: "ri-time-fill",
    label: "Abandonnée",
  },
  AUTHORIZED: {
    icon: "ri-check-fill",
    label: "Déclaration finalisée",
  },
  REJECTED: {
    icon: "ri-error-warning-fill",
    label: "Refus",
  },
  WITHDRAWN: {
    icon: "ri-close-fill",
    label: "Retirée du marché",
  },
}

export const roleNameDisplayNameMapping = { DeclarantRole: "déclarant", SupervisorRole: "gestionnaire" }

export const tabTitles = (components, useSubmission = false) => {
  const idx = (x) => components.findIndex((y) => (y.name || y.__name) === x)
  const titleMap = {
    IdentityTab: {
      title: "Identité",
      icon: "ri-shield-user-line",
      tabId: `tab-${idx("IdentityTab")}`,
      panelId: `tab-content-${idx("IdentityTab")}`,
    },
    DeclarationSummary: {
      title: "Produit",
      icon: "ri-flask-line",
      tabId: `tab-${idx("DeclarationSummary")}`,
      panelId: `tab-content-${idx("DeclarationSummary")}`,
    },
    DecisionTab: {
      title: "Décision",
      icon: "ri-checkbox-circle-line",
      tabId: `tab-${idx("DecisionTab")}`,
      panelId: `tab-content-${idx("DecisionTab")}`,
    },
    HistoryTab: {
      title: "Historique",
      icon: "ri-chat-3-line",
      tabId: `tab-${idx("HistoryTab")}`,
      panelId: `tab-content-${idx("HistoryTab")}`,
    },
    SummaryTab: {
      title: useSubmission ? "Soumettre" : "Résumé",
      icon: useSubmission ? "ri-mail-send-line" : "ri-survey-line",
      tabId: `tab-${idx("SummaryTab")}`,
      panelId: `tab-content-${idx("SummaryTab")}`,
    },
    ProductTab: {
      title: "Produit",
      icon: "ri-capsule-fill",
      tabId: `tab-${idx("ProductTab")}`,
      panelId: `tab-content-${idx("ProductTab")}`,
    },
    CompositionTab: {
      title: "Composition",
      icon: "ri-test-tube-line",
      tabId: `tab-${idx("CompositionTab")}`,
      panelId: `tab-content-${idx("CompositionTab")}`,
    },
    AttachmentTab: {
      title: "Pièces jointes",
      icon: "ri-file-text-line",
      tabId: `tab-${idx("AttachmentTab")}`,
      panelId: `tab-content-${idx("AttachmentTab")}`,
    },
    NewElementTab: {
      title: "Nouveaux ingrédients",
      icon: "ri-flask-line",
      tabId: `tab-${idx("NewElementTab")}`,
      panelId: `tab-content-${idx("NewElementTab")}`,
    },
    WithdrawalTab: {
      title: "Retirer du marché",
      icon: "ri-close-fill",
      tabId: `tab-${idx("WithdrawalTab")}`,
      panelId: `tab-content-${idx("WithdrawalTab")}`,
    },
    VisaValidationTab: {
      title: "Visa / Signature",
      icon: "ri-checkbox-circle-line",
      tabId: `tab-${idx("VisaValidationTab")}`,
      panelId: `tab-content-${idx("VisaValidationTab")}`,
    },
  }
  return components.map((x) => titleMap[x.__name || x.name])
}

export const orderingOptions = [
  { value: "modificationDate", text: "Date de modification" },
  { value: "-modificationDate", text: "Date de modification (descendant)" },
  { value: "name", text: "Nom du produit" },
  { value: "-name", text: "Nom du produit (descendant)" },
  { value: "responseLimitDate", text: "Date limite de réponse" },
  { value: "-responseLimitDate", text: "Date limite de réponse (descendant)" },
]

export const articleOptionsWith15Subtypes = [
  { value: "ART_15", text: "Article 15", shortText: "15" },
  { value: "ART_15_WARNING", text: "Article 15 vigilance", shortText: "15 vig." },
  { value: "ART_15_HIGH_RISK_POPULATION", text: "Article 15 population à risque", shortText: "15 pop." },
  { value: "ART_16", text: "Article 16", shortText: "16" },
  { value: "ART_18", text: "Article 18", shortText: "18" },
  { value: "ANSES_REFERAL", text: "Saisine ANSES", shortText: "Saisine ANSES" },
]

export const articleOptions = [
  { value: "ART_15", text: "Article 15", shortText: "15" },
  { value: "ART_15_WARNING", text: "Article 15", shortText: "15" },
  { value: "ART_15_HIGH_RISK_POPULATION", text: "Article 15", shortText: "15" },
  { value: "ART_16", text: "Article 16", shortText: "16" },
  { value: "ART_18", text: "Article 18", shortText: "18" },
  { value: "ANSES_REFERAL", text: "Saisine ANSES", shortText: "Saisine ANSES" },
]

export const typeOptions = [
  { value: "plant", text: "Plante" },
  { value: "microorganism", text: "Microorganisme" },
  { value: "substance", text: "Substance" },
  { value: "ingredient", text: "Autre ingrédient" },
]

export const authorizationModesMapping = {
  FR: "Utilisable en France",
  EU: "Autorisé dans un État membre de l'UE ou EEE",
}

export const populationCategoriesMapping = {
  AGE: {
    label: "Âge",
  },
  MEDICAL: {
    label: "Conditions médicales spécifiques",
  },
  PREGNANCY: {
    label: "Grossesse et allaitement",
  },
  MEDICAMENTS: {
    label: "Interactions médicamenteuses",
  },
  OTHER: {
    label: "Autres",
  },
}

export const getAuthorizationModeInFrench = (type) => {
  return authorizationModesMapping[type] || null
}

export const blockingReasons = [
  {
    title: "Le produit ne répond pas à la définition du complément alimentaire",
    items: [
      "Forme assimilable à un aliment courant",
      "Recommandations d'emploi incompatibles",
      "Composition (source concentrée, ...)",
      "Autre raison pour laquelle le produit ne répond pas à la définition du complément alimentaire",
    ],
  },
  {
    title: "Le produit répond à la définition du médicament",
    items: ["Médicament par fonction", "Médicament par présentation", "Sevrage tabagique"],
  },
  {
    title: "Les procédures ne sont pas respectées",
    items: [
      "Présence d'un Novel Food",
      "Présence d'une forme d'apport en nutriments non autorisée",
      "Demande en article 17 attendue",
      "Demande en article 18 attendue",
    ],
  },
  {
    title: "Le dossier n'est pas recevable",
    items: [
      "Incohérences entre le dossier et l'étiquetage",
      "Informations manquantes",
      "Absence de preuve de reconnaissance mutuelle",
      "Absence ou non conformité de l'étiquetage",
      "Autre motif d'irrecevabilité",
    ],
  },
  {
    title: "Le complément alimentaire n'est pas acceptable",
    items: ["Existence d'un risque"],
  },
]

export const decisionCategories = [
  {
    value: "approve",
    title: "J’envoie l’attestation de déclaration",
    icon: "ri-checkbox-circle-fill",
    description: "La déclaration est conforme et peut être transmise.",
    color: "green",
  },
  {
    value: "modify",
    title: "Des changements sont nécessaires",
    icon: "ri-close-circle-fill",
    description: "La déclaration ne peut pas être transmise en l'état.",
    color: "red",
  },
]

export const allActivities = [
  {
    label: "Fabricant",
    value: "FABRICANT",
    hint: "Le fabricant est responsable de la production des compléments alimentaires.",
  },
  {
    label: "Façonnier",
    value: "FAÇONNIER",
    hint: "Le façonnier (ou sous-traitant) produit des compléments alimentaires pour le compte d'autres marques.",
  },
  {
    label: "Importateur",
    value: "IMPORTATEUR",
    hint: "L'importateur est responsable de l'introduction de compléments alimentaires provenant d'un pays hors UE, sur le marché français.",
  },
  {
    label: "Introducteur",
    value: "INTRODUCTEUR",
    hint: "L'introducteur est responsable de l'introduction de compléments alimentaires provenant d'un pays de l'UE, sur le marché français.",
  },
  {
    label: "Conseil",
    value: "CONSEIL",
    hint: "Ce rôle peut être tenu par des organismes spécialisés (type cabinet de conseil) qui fournissent des expertises et des conseils aux autres acteurs de la chaîne.",
  },
  {
    label: "Distributeur",
    value: "DISTRIBUTEUR",
    hint: "Le distributeur achète des compléments alimentaires pour les revendre aux détaillants ou directement aux consommateurs.",
  },
]

export const getCompanyActivitiesString = (activities) =>
  activities
    .map((x) => allActivities.find((y) => y.value === x).label)
    .sort((a, b) => a.localeCompare(b))
    .join(", ")
