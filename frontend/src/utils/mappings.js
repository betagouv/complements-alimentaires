const flip = (data) => Object.fromEntries(Object.entries(data).map(([key, value]) => [slugify(value), key]))

export const slugify = (data) => data?.replace(" ", "-").replace("'", "-").toLowerCase()

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

export const getApiType = (type) => (type === "form_of_supply" ? "forms-of-supply" : `${type.replace("_", "-")}s`)

export const typesMapping = {
  plant: "Plante",
  microorganism: "Micro-organisme",
  form_of_supply: "Forme d'apport",
  aroma: "Arôme",
  additive: "Additif",
  active_ingredient: "Ingredient actif",
  non_active_ingredient: "Ingredient non actif",
  substance: "Substance",
}

export const frenchSlugToTypeMapping = flip(typesMapping)

export const getTypeInFrench = (type) => {
  return typesMapping[type] || null
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
  OBSERVATION: {
    icon: "ri-file-search-fill",
    label: "En observation",
  },
  ABANDONED: {
    icon: "ri-time-fill",
    label: "Abandonnée",
  },
  AUTHORIZED: {
    icon: "ri-check-fill",
    label: "Autorisée",
  },
}

export const roleNameDisplayNameMapping = { DeclarantRole: "déclarant", SupervisorRole: "gestionnaire" }

export const statusFilterOptions = [
  { value: "", text: "Tous les statuts" },
  { value: "AWAITING_INSTRUCTION", text: "En attente d'instruction" },
  { value: "ONGOING_INSTRUCTION", text: "En cours d'instruction" },
  { value: "OBSERVATION", text: "Observation" },
  { value: "ABANDON", text: "Abandon" },
  { value: "AUTHORIZED", text: "Autorisé" },
]
