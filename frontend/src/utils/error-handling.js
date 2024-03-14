import useToaster from "@/composables/use-toaster"
const { addErrorMessage } = useToaster()

export const handleError = async (response, error) => {
  // Do nothing if there is no error
  if (!error.value) {
    return
  }

  // Handle display of the error (directly on the form or in a toast)
  // https://vuelidate-next.netlify.app/advanced_usage.html#config-with-composition-api
  const backErrorData = await response.value.json()
  if (backErrorData.display == "global") {
    addErrorMessage(backErrorData.detail)
  } else if (backErrorData.display == "non_field") {
    return { non_field: backErrorData.detail }
  } else if (backErrorData.display == "field") {
    return { [backErrorData.fieldName]: backErrorData.detail }
  }

  // NOTE FOR LATER: auto logout (in case of 401) could be handled here
  // NOTE FOR LATER: timeout could be handled ehre
}
