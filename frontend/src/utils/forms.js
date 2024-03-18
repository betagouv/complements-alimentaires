import { helpers, required, email } from "@vuelidate/validators"

/* Using vuelidate validation, return the first error message, or "" if no error found. */
export const firstErrorMsg = (v, fieldName) => (v[fieldName].$error ? v[fieldName].$errors[0].$message : null)

// reusable field errors
export const errorRequiredField = { required: helpers.withMessage("Ce champ doit être rempli", required) }
export const errorRequiredEmail = {
  required: helpers.withMessage("Ce champ doit être rempli", required),
  email: helpers.withMessage("Ce champ doit contenir un e-mail valide", email),
}
