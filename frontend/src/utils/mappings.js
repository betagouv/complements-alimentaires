const flip = (data) => Object.fromEntries(Object.entries(data).map(([key, value]) => [value, key]))

export const getTypeIcon = (type) => {
  const iconMapping = {
    plant: "ri-plant-line",
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
  microorganism: "Micro-organisme",
  form_of_supply: "Forme d'apport", // nutrient: "Nutriment"
  aroma: "Arôme",
  additive: "Additif",
  active_ingredient: "Ingredient actif",
  non_active_ingredient: "Ingredient non actif", // TODO : merger ces 2 types en 1 et n'utiliser que le label "actif"/"inactif"
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
}
export const getTypeInFrench = (type) => {
  return typesMapping[type] || null
}

export const slugify = (data) => data?.replaceAll(" ", "-").replaceAll("'", "-").toLowerCase()

export const unSlugify = (typeSlug) => {
  return frontToAPITypesSlugMapping[typeSlug] || null
}

export const getApiType = (type) => {
  switch (type) {
    case "form_of_supply":
    case "aroma":
    case "additive":
    case "active_ingredient":
    case "non_active_ingredient":
      return "other-ingredients"
    default:
      return `${type.replace("_", "-")}s`
  }
}

export const statusProps = {
  DRAFT: {
    icon: "ri-pencil-fill",
    label: "Brouillon",
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
    label: "Autorisée",
  },
  REJECTED: {
    icon: "ri-error-warning-fill",
    label: "Refusée",
  },
}

export const roleNameDisplayNameMapping = { DeclarantRole: "déclarant", SupervisorRole: "gestionnaire" }

export const statusFilterOptions = [
  { value: "", text: "Tous les statuts" },
  { value: "AWAITING_INSTRUCTION", text: "En attente d'instruction" },
  { value: "ONGOING_INSTRUCTION", text: "En cours d'instruction" },
  { value: "AWAITING_VISA", text: "En attente de visa" },
  { value: "ONGOING_VISA", text: "Visa en cours" },
  { value: "OBJECTION", text: "Objection" },
  { value: "OBSERVATION", text: "Observation" },
  { value: "ABANDONED", text: "Abandon" },
  { value: "AUTHORIZED", text: "Autorisée" },
  { value: "REJECTED", text: "Refusée" },
]
