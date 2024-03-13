<template>
  <DsfrHeader :logo-text="logoText" service-title="Compléments alimentaires" :quickLinks="quickLinks">
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
import useToaster from "@/composables/use-toaster"
import { useRouter } from "vue-router"

defineProps({ logoText: Array })

const environment = window.ENVIRONMENT
const { addMessage, addUnknownErrorMessage } = useToaster()
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
  const { error } = await useFetch("/api/v1/logout/").post()
  if (error.value) {
    addUnknownErrorMessage()
  } else {
    await store.resetInitialData()
    router.replace({ name: "LandingPage" })
    addMessage({
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
