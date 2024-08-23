<template>
  <DsfrHeader :logo-text="logoText" :quickLinks="quickLinks">
    <template #operator>
      <div class="flex items-center">
        <a href="/">
          <img :src="require('@/assets/logo.svg')" alt="Logo Compl'Alim" class="h-20" />
        </a>

        <DsfrBadge v-if="environment === 'dev'" :label="environment" type="info" />
        <DsfrBadge v-if="environment === 'demo'" :label="environment" type="new" />
        <DsfrBadge v-if="environment === 'staging'" :label="environment" type="warning" />
      </div>
    </template>
    <template #mainnav>
      <div class="flex justify-between whitespace-nowrap">
        <DsfrNavigation :nav-items="navItems" />
        <DsfrNavigation v-if="store.loggedUser" :nav-items="loggedOnlyNavItems" />
      </div>
    </template>
  </DsfrHeader>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { logOut } from "@/utils/auth"

defineProps({ logoText: Array })

const environment = window.ENVIRONMENT
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
    text: "Tableau de bord",
  },
]

const quickLinks = computed(() => {
  if (store.loggedUser)
    return [
      {
        label: "Se déconnecter",
        icon: "ri-logout-circle-line",
        button: true,
        onClick: () => logOut(),
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
