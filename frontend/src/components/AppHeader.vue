<template>
  <DsfrHeader :logo-text="logoText" service-title="Compléments alimentaires" :quickLinks="quickLinks">
    <template #mainnav>
      <DsfrNavigation :nav-items="navItems" />
    </template>
  </DsfrHeader>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useStore } from "vuex"

const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "Alimentaire"]
const store = useStore()
const navItems = [
  {
    to: "/",
    text: "Accueil",
  },
  {
    to: "/blog",
    text: "Blog",
  },
]
const quickLinks = computed(function () {
  if (store.state.loggedUser)
    return [
      {
        label: "Se déconnecter",
        icon: "ri-account-circle-line",
        href: `${window.location.protocol}//${window.location.host}/se-deconnecter`,
      },
    ]
  else return []
})
onMounted(() => {
  store.dispatch("fetchLoggedUser")
})
</script>
