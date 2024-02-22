export const isoToPrettyDate = (isoDate) =>
  // e.g. 2024-02-22 -> 22 févr. 2024
  new Date(isoDate).toLocaleDateString("fr-FR", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
