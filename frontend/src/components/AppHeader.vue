<template>
  <DsfrHeader :logo-text="logoText" :homeTo="{ name: 'LandingPage' }" :quickLinks="quickLinks">
    <template #operator>
      <div class="flex items-center">
        <img :src="require('@/assets/logo.svg')" alt="Compl'Alim" class="h-20" />

        <div class="hidden sm:inline">
          <DsfrBadge v-if="environment === 'dev'" :label="environment" type="info" />
          <DsfrBadge v-if="environment === 'demo'" :label="environment" type="new" />
          <DsfrBadge v-if="environment === 'staging'" :label="environment" type="warning" />
        </div>
      </div>
    </template>
    <template #mainnav>
      <DsfrNavigation :nav-items="navItems" :class="{ 'last-link-right': store.loggedUser }" />
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
const navItems = computed(() => {
  const links = [
    {
      to: "/accueil",
      text: "Accueil",
    },
    {
      to: "/entreprises",
      text: "Recherche ingrédients",
    },
    {
      to: "/blog",
      text: "Ressources",
    },
    {
      to: "/faq",
      text: "FAQ",
    },
  ]
  if (store.loggedUser)
    links.push({
      to: "/tableau-de-bord",
      text: "Tableau de bord",
    })
  return links
})

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

<style>
.fr-header__menu:not(.fr-modal--opened) nav.last-link-right > ul > li:last-child {
  margin-left: auto;
}
</style>
