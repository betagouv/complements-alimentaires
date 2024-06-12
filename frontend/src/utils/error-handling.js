import useToaster from "@/composables/use-toaster"
import router from "@/router/index"
const { addErrorMessage } = useToaster()

export const handleError = async (response) => {
  // Do nothing if there is actually no error
  if (response.value.ok) {
    return
  }

  // Redirect to a dedicated page in case of 404
  // NOTE: we could handle this at back-end level too, if we'd need more granularity.
  if (response.value.status == 404) {
    router.replace({ name: "NotFound" })
    return
  }

  const contentType = response.value.headers.get("content-type")
  const hasJSON = contentType && contentType.startsWith("application/json")
  if (!hasJSON) {
    addErrorMessage("Une erreur s'est produite, merci de réessayer ultérieurement")
    console.error(response.value)
    return
  }

  // Handle display of the errors (directly on the form or in a toast)
  // https://vuelidate-next.netlify.app/advanced_usage.html#config-with-composition-api
  const backErrorData = await response.value.json()
  if (backErrorData.globalError) {
    // show an error toast
    addErrorMessage(backErrorData.globalError)
  }
  // Return other errors to be handled by Vuelidate directly (and "extra" parameters to get additional data)
  // If you don't have a form and expect global errors only, just ignore the result of this function when called.
  return {
    nonFieldErrors: backErrorData.nonFieldErrors,
    fieldErrors: backErrorData.fieldErrors,
    ...backErrorData.fieldErrors,
    extra: backErrorData.extra,
  }

  // TODO LATER: auto logout (in case of 401) could be handled here
  // TODO LATER: timeout could be handled here too
}
