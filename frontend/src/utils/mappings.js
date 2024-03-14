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
