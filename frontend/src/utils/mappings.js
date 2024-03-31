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

export const countries = [
  { text: "France", value: "FR" },
  { text: "Allemagne", value: "DE" },
  { text: "Autriche", value: "AT" },
  { text: "Belgique", value: "BE" },
  { text: "Bulgarie", value: "BG" },
  { text: "Chypre", value: "CY" },
  { text: "Croatie", value: "HR" },
  { text: "Danemark", value: "DK" },
  { text: "Espagne", value: "ES" },
  { text: "Estonie", value: "EE" },
  { text: "Finlande", value: "FI" },
  { text: "Grèce", value: "GR" },
  { text: "Hongrie", value: "HU" },
  { text: "Irlande", value: "IE" },
  { text: "Irlande du Nord", value: "NI" },
  { text: "Islande", value: "IS" },
  { text: "Italie", value: "IT" },
  { text: "Lettonie", value: "LV" },
  { text: "Liechtenstein", value: "LI" },
  { text: "Lituanie", value: "LT" },
  { text: "Luxembourg", value: "LU" },
  { text: "Malte", value: "MT" },
  { text: "Norvège", value: "NO" },
  { text: "Pays-Bas", value: "NL" },
  { text: "Pologne", value: "PL" },
  { text: "Portugal", value: "PT" },
  { text: "Roumanie", value: "RO" },
  { text: "Slovaquie", value: "SK" },
  { text: "Slovénie", value: "SI" },
  { text: "Suède", value: "SE" },
  { text: "République Tchèque", value: "CZ" },
]
