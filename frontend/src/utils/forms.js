import { helpers, required, email, numeric, integer, maxLength } from "@vuelidate/validators"

/* Using vuelidate validation, return the first error message, or "" if no error found. */
export const firstErrorMsg = (v, fieldName) => (v[fieldName]?.$error ? v[fieldName].$errors[0].$message : null)

// reusable field errors
const REQUIRED = helpers.withMessage("Ce champ doit être rempli", required)
export const errorRequiredField = { required: REQUIRED }
export const errorRequiredEmail = {
  required: REQUIRED,
  email: helpers.withMessage("Ce champ doit contenir un e-mail valide", email),
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

export const toOptions = (list) => {
  const options =
    (list || [])
      .map((x) => ({ value: x.id, text: x.name.split(" (à préciser)")[0] })) // Transforme la réponse API en options pour les champs select
      .sort((a, b) => a.text.localeCompare(b.text)) || [] // Triage alphabétique
  options.unshift({ disabled: true, text: "---------" })
  options.unshift({ value: "", text: "Tout afficher" })
  return options
}
