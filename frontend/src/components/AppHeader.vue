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
import { computed, onMounted, watch } from "vue"
import { useStore } from "vuex"
import { useRoute } from "vue-router"

const route = useRoute()

const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "Alimentaire"]
const environment = window.ENVIRONMENT
const store = useStore()
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
  if (store.state.loggedUser)
    return [
      {
        label: "Se déconnecter",
        icon: "ri-logout-box-r-line",
        to: { query: { "confirmation-deconnexion": true }, replace: true },
      },
    ]
  else return []
})
onMounted(() => {
  store.dispatch("fetchLoggedUser")
})
watch(
  () => route.query["confirmation-deconnexion"],
  (newValue) => {
    const headers = {
      "X-CSRFToken": window.CSRF_TOKEN || "",
      "Content-Type": "application/json",
    }
    if (newValue)
      return fetch(`/se-deconnecter`, { method: "POST", headers, redirect: "follow" }).then((response) => {
        if (response.redirected) window.location.href = response.url
      })
  }
)
</script>
