import { helpers, required, email, numeric, integer, maxLength } from "@vuelidate/validators"

/* Using vuelidate validation, return the first error message, or "" if no error found. */
export const firstErrorMsg = (v, fieldName) => (v[fieldName]?.$error ? v[fieldName].$errors[0].$message : null)

// reusable field errors
const REQUIRED = helpers.withMessage("Ce champ doit être rempli", required)
export const errorRequiredField = { required: REQUIRED }
export const errorRequiredEmail = {
  required: REQUIRED,
  email: helpers.withMessage("L'e-mail doit être en format valide (ex : nom@entreprise.com)", email),
}
export const errorNumeric = {
  numeric: helpers.withMessage("Ce champ doit être un chiffre", numeric),
}
export const errorInteger = {
  integer: helpers.withMessage("Ce champ doit être un chiffre entier", integer),
}
export const errorMaxStringLength = (max) => {
  return {
    maxLength: helpers.withMessage(
      ({ $params, $model }) => `Ce champ ne doit pas dépasser ${$params.max} caractères, ${$model.length} actuel`,
      maxLength(max)
    ),
  }
}
export const errorRequiredPhoneNumber = {
  required: REQUIRED,
  ...errorMaxStringLength(16), // le format E164 demande un + et un max de 15 chiffres
  phoneNumber: helpers.withMessage("Le numéro doit être en format valide (ex : +33612345678)", (phoneNumber) =>
    /^\+[1-9]\d{1,14}$/.test(phoneNumber)
  ),
}

export const getAllIndexesOfRegex = (array, regex) => {
  return array.map((obj) => (regex.test(obj.name) ? obj.id : -1)).filter((i) => i != -1)
}

// met les choix "Autre % (à préciser)" en dernier dans la liste
export const pushOtherChoiceFieldAtTheEnd = (choices) => {
  const otherObjsIds = getAllIndexesOfRegex(choices, /Autre.*(à préciser)/)
  if (otherObjsIds) {
    const otherObjs = choices.filter((obj) => otherObjsIds.includes(obj.id))
    choices = choices.filter((obj) => !otherObjsIds.includes(obj.id))
    choices.push(...otherObjs)
  }
  return choices
}

export const transformArrayByColumn = (arr, numberOfColumns) => {
  /*
  Transforme l'affichage d'un tableau en son équivalent d'affichage par colonnes. Par exemple,
  [0, 1, 2, 3, 4, 5] en trois colonnes s'afficherait :
  ---
  0, 1, 2
  3, 4, 5
  ---
  En passant par cette fonction, l'output serait :
  [0, 2, 4, 1, 3, 5], qu'en trois colonnes s'afficherait :
  ---
  0, 2, 4
  1, 3, 5
  ---
  Privilégiant ainsi une lecture verticale.
  Utile pour l'affichage des checkboxes dans des grilles de colonnes.
  */
  const result = []
  if (!arr) return result
  const fullRows = Math.floor(arr.length / numberOfColumns) // Les rangées pleines
  const remainingItems = arr.length % numberOfColumns // Les éléments qui resterons dans une dernière rangée

  const numRows = remainingItems > 0 ? fullRows + 1 : fullRows

  for (let row = 0; row < numRows; row++) {
    for (let col = 0; col < numberOfColumns; col++) {
      const index = col * fullRows + Math.min(col, remainingItems) + row
      if (row < fullRows || (row === fullRows && col < remainingItems)) result.push(arr[index])
    }
  }

  return result
}

export const checkboxColumnNumbers = { sm: 1, md: 2, lg: 2, xl: 3 }

export const toOptions = (list) => {
  const options =
    (list || [])
      .map((x) => ({ value: x.id, text: x.name.split(" (à préciser)")[0] })) // Transforme la réponse API en options pour les champs select
      .sort((a, b) => a.text.localeCompare(b.text)) || [] // Triage alphabétique
  options.unshift({ disabled: true, text: "---------" })
  options.unshift({ value: "", text: "Tout afficher" })
  return options
}
