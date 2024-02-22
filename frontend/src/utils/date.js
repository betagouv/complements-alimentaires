const frLocale = "fr-FR"

// e.g. with default: 2024-02-22T16:43:57+01:00 -> 22 févr. 2024
export const isoToPrettyDate = (
  isoDate,
  options = {
    year: "numeric",
    month: "short",
    day: "numeric",
    weekday: undefined,
  }
) => new Date(isoDate).toLocaleDateString(frLocale, options)

// e.g. 2024-02-22T16:43:57+01:00 -> 16h43
export const isoToPrettyTime = (isoDate) => {
  const hour = new Date(isoDate).toLocaleString(frLocale, { hour: "numeric" })
  const minutes = new Date(isoDate).toLocaleString(frLocale, { minute: "2-digit" })
  return `${hour}${minutes}`.replace(" ", "")
}
