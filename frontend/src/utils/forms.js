/* Using vuelidate validation, return the first error message, or "" if no error found. */
export const firstErrorMsg = (v, fieldName) => (v[fieldName].$error ? v[fieldName].$errors[0].$message : null)
