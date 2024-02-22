<template>
  <DsfrHeader :logo-text="logoText" service-title="Compléments alimentaires" :quickLinks="quickLinks">
    <template v-if="environment != 'prod'" #operator>
      <DsfrBadge v-if="environment === 'dev'" :label="environment" type="info" />
      <DsfrBadge v-else-if="environment === 'demo'" :label="environment" type="new" />
      <DsfrBadge v-else :label="environment" type="warning" />
    </template>
    <template #mainnav>
      <DsfrNavigation :nav-items="navItems" />
    </template>
  </DsfrHeader>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { headers } from "@/utils"

const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "Alimentaire"]
const environment = window.ENVIRONMENT
const store = useRootStore()
const navItems = [
  {
    to: "/",
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
const quickLinks = computed(function () {
  if (store.loggedUser)
    return [
      {
        label: "Se déconnecter",
        icon: "ri-logout-box-r-line",
        button: true,
        onClick: logout,
      },
    ]
  else return []
})
const logout = () => {
  return fetch(`/se-deconnecter`, { method: "POST", headers, redirect: "follow" }).then((response) => {
    if (response.redirected) window.location.href = response.url
  })
}
</script>
