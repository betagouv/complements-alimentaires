import useToaster from "@/composables/use-toaster"
import router from "@/router/index"
const { addErrorMessage } = useToaster()

export const handleError = async (response, error) => {
  // Do nothing if there is actually no error
  if (!error.value) {
    return
  }

  // Redirect to a dedicated page in case of 404
  // NOTE: we could handle this at back-end level too, if we'd need more granularity.
  if (response.value.status == 404) {
    router.replace({ name: "NotFound" })
    return
  }

  // Handle display of the errors (directly on the form or in a toast)
  // https://vuelidate-next.netlify.app/advanced_usage.html#config-with-composition-api
  const backErrorData = await response.value.json()
  if (backErrorData.globalError) {
    // show an error toast
    addErrorMessage(backErrorData.globalError)
  }
  // return other errors to be handled by Vuelidate directly
  return { nonFieldErrors: backErrorData.nonFieldErrors, ...backErrorData.fieldErrors }

  // TODO LATER: auto logout (in case of 401) could be handled here
  // TODO LATER: timeout could be handled here too
}
