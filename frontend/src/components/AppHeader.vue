<template>
  <DsfrHeader :logo-text="logoText" service-title="Compl'Alim" :quickLinks="quickLinks">
    <template v-if="environment != 'prod'" #operator>
      <DsfrBadge v-if="environment === 'dev'" :label="environment" type="info" />
      <DsfrBadge v-else-if="environment === 'demo'" :label="environment" type="new" />
      <DsfrBadge v-else :label="environment" type="warning" />
    </template>
    <template #mainnav>
      <div class="flex justify-between">
        <DsfrNavigation :nav-items="navItems" />
        <DsfrNavigation v-if="store.loggedUser" :nav-items="loggedOnlyNavItems" />
      </div>
    </template>
  </DsfrHeader>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"

defineProps({ logoText: Array })

const environment = window.ENVIRONMENT
const router = useRouter()
const store = useRootStore()
const navItems = [
  {
    to: "/accueil",
    text: "Accueil",
  },
  {
    to: "/entreprises",
    text: "Entreprises",
  },
  {
    to: "/blog",
    text: "Blog",
  },
]
const loggedOnlyNavItems = [
  {
    to: "/tableau-de-bord",
    text: "Dashboard",
  },
]

const logOut = async () => {
  const { response } = await useFetch("/api/v1/logout/", { headers: headers() }).post()
  await handleError(response)
  if (response.value.ok) {
    await router.replace({ name: "LandingPage" })
    await store.resetInitialData()
    useToaster().addMessage({
      type: "success",
      title: "Vous êtes déconnecté",
      description: "Vous avez été déconnecté de la plateforme.",
    })
  }
}

const quickLinks = computed(() => {
  if (store.loggedUser)
    return [
      {
        label: "Se déconnecter",
        icon: "ri-logout-circle-line",
        button: true,
        onClick: logOut,
      },
    ]
  else
    return [
      {
        label: "Se connecter",
        icon: "ri-login-circle-line",
        to: "/connexion",
      },
      {
        label: "S'enregistrer",
        icon: "ri-account-circle-line",
        to: "/inscription",
      },
    ]
})
</script>
