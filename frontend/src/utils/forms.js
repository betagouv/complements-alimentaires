import { helpers, required, email } from "@vuelidate/validators"

/* Using vuelidate validation, return the first error message, or "" if no error found. */
export const firstErrorMsg = (v, fieldName) => (v[fieldName]?.$error ? v[fieldName].$errors[0].$message : null)

// reusable field errors
export const errorRequiredField = { required: helpers.withMessage("Ce champ doit être rempli", required) }
export const errorRequiredEmail = {
  required: helpers.withMessage("Ce champ doit être rempli", required),
  email: helpers.withMessage("Ce champ doit contenir un e-mail valide", email),
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
