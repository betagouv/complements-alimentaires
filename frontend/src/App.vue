<template>
  <AppHeader />
  <router-view></router-view>
  <DsfrFooter :logo-text="logoText" :mandatory-links="footerLinks">
    <template v-slot:description>
      <p>Compléments alimentaires</p>
    </template>
  </DsfrFooter>
</template>

<script setup>
import { watch } from "vue"
import { useRoute } from "vue-router"
import AppHeader from "@/components/AppHeader.vue"

const route = useRoute()

const footerLinks = [
  {
    label: "Mentions légales",
    to: { name: "LegalNotices" },
  },
  {
    label: "Politique de confidentialité",
    to: { name: "PrivacyPolicy" },
  },
  {
    label: "Conditions générales d'utilisation",
    to: { name: "CGU" },
  },
]

watch(route, (to) => {
  const suffix = "Compléments alimentaires"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
})
</script>

<style>
.fr-pagination__list {
  justify-content: center;
}
</style>
