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

export const roleNameDisplayNameMapping = { Declarant: "déclarant", Supervisor: "gestionnaire" }
