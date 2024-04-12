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

export const timeAgo = (date) => {
  if (typeof date === "string") date = new Date(date)
  const prefix = "il y a"

  const seconds = (new Date() - date) / 1000
  if (seconds < 60) return "à l'instant"

  const minutes = Math.round(seconds / 60)
  if (minutes < 60) return `${prefix} ${minutes} m`

  const hours = Math.round(seconds / 3600)
  if (hours < 24) return `${prefix} ${hours} h`

  const days = Math.round(seconds / 3600 / 24)
  if (days < 120) return date.toLocaleString("fr-FR", { month: "long", day: "numeric" })
  return date.toLocaleString("fr-FR", { month: "long", day: "numeric", year: "numeric" })
}
