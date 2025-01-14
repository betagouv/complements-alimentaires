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
  const numRows = Math.ceil(arr.length / numberOfColumns)

  for (let row = 0; row < numRows; row++) {
    for (let col = 0; col < numberOfColumns; col++) {
      const index = col * numRows + row
      if (index < arr.length) result.push(arr[index])
    }
  }
  return result
}
