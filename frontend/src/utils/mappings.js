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
    label: "En attente",
  },
  AWAITING_PRODUCER: {
    icon: "ri-error-warning-fill",
    label: "Action requise",
  },
  REJECTED: {
    icon: "ri-close-fill",
    label: "Rejetée",
  },
  APPROVED: {
    icon: "ri-check-fill",
    label: "Validée",
  },
}

export const roleNameDisplayNameMapping = { DeclarantRole: "déclarant", SupervisorRole: "gestionnaire" }
