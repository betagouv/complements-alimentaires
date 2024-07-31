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
      title: "Nouveaux éléments",
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
