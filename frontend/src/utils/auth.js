import { useFetch } from "@/utils/data-fetching"
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
  const { data, response } = await useFetch(`logout/`, { headers: headers() }).post().json()
  await handleError(response)
  if (response.value.ok) {
    if (data.value?.logoutUrl) {
      // Déconnexion OIDC : on navigue vers le fournisseur pour qu'il termine la session SSO.
      // Il redirige ensuite vers /api/logout-callback/ qui effectue la déconnexion Django.
      window.location.href = data.value.logoutUrl
      return
    }
    await router.replace({ name: redirectRouteName, query: routeQueryParams })
    await useRootStore().resetInitialData()
    useToaster().addSuccessMessage(message)
  }
}
