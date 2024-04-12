import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"
import router from "@/router/index"
import { useRootStore } from "@/stores/root"

export const logOut = async (
  message = "Vous avez été déconnecté de la plateforme.",
  redirectRouteName = "LandingPage",
  routeQueryParams = {}
) => {
  const { response } = await useFetch("/api/v1/logout/", { headers: headers() }).post()
  await handleError(response)
  if (response.value.ok) {
    await router.replace({ name: redirectRouteName, query: routeQueryParams })
    await useRootStore().resetInitialData()
    useToaster().addSuccessMessage(message)
  }
}
