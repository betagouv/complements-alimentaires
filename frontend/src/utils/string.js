export const truncateMiddle = (str, maxLength) => {
  // Cette fonction permet d'assurer qu'une chaîne de caractères ne dépasse pas une longeur
  // choisie en insérant « … » au milieu de la chaîne en remplacement des caractères qui
  // la font dépasser. Par exemple, la chaîne "Issy-les-Moulineaux" en longeur 5 deviendrait
  // "Is…ux"

  if (str.length <= maxLength) return str

  const charsToKeep = Math.floor((maxLength - 1) / 2)
  const start = str.slice(0, charsToKeep)
  const end = str.slice(-charsToKeep)

  return `${start}…${end}`
}
