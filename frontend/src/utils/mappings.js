export const getTypeIcon = (type) => {
  const mapping = {
    plant: "ri-plant-line",
    microorganism: "ri-microscope-line",
    ingredient: "ri-flask-line",
    substance: "ri-test-tube-line",
  }
  return mapping[type] || "ri-drop-line"
}

export const getType = (type) => {
  const mapping = {
    plant: "Plante",
    microorganism: "Micro-organisme",
    ingredient: "Ingredient",
    substance: "Substance",
    nutrient: "Nutriment",
    additive: "Additif",
    aroma: "Arôme",
  }
  return mapping[type] || null
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
