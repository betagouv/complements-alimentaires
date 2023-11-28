<template>
  <DsfrHeader :logo-text="logoText" service-title="Compléments alimentaires" :quickLinks="quickLinks" />
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useStore } from "vuex"

const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "Alimentaire"]
const store = useStore()
const quickLinks = computed(function () {
  if (store.state.loggedUser)
    return [
      {
        label: "Se déconnecter",
        to: "/se-deconnecter",
        icon: "ri-account-circle-line",
      },
    ]
  else return []
})
onMounted(() => {
  store.dispatch("fetchLoggedUser")
})
</script>
