import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"
import router from "@/router/index"
import { useRootStore } from "@/stores/root"

export const logOut = async () => {
  const { response } = await useFetch("/api/v1/logout/", { headers: headers() }).post()
  await handleError(response)
  if (response.value.ok) {
    await router.replace({ name: "LandingPage" })
    await useRootStore().resetInitialData()
    useToaster().addMessage({
      type: "success",
      title: "Vous êtes déconnecté",
      description: "Vous avez été déconnecté de la plateforme.",
    })
  }
}
