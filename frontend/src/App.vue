<template>
  <AppHeader :logo-text="logoText" />
  <router-view></router-view>
  <DsfrFooter
    :logo-text="logoText"
    :cookiesLink="{ name: 'CookiesInfoPage' }"
    :legalLink="{ name: 'LegalNoticesPage' }"
    :personalDataLink="{ name: 'PrivacyPolicyPage' }"
    :afterMandatoryLinks="[{ label: 'Conditions générales d’utilisation', to: { name: 'CGUPage' } }]"
  >
    <template v-slot:description>
      <p>Compl'Alim</p>
    </template>
  </DsfrFooter>
  <AppToaster :messages="messages" @close-message="removeMessage($event)" />
</template>

<script setup>
import { watch } from "vue"
import { useRoute } from "vue-router"
import AppToaster from "@/components/AppToaster.vue"
import useToaster from "@/composables/use-toaster"
import AppHeader from "@/components/AppHeader.vue"

const route = useRoute()
const { messages, removeMessage } = useToaster()
const logoText = ["Ministère", "de l’Agriculture", "de la Souveraineté", "Alimentaire et de la forêt"]

watch(route, (to) => {
  const suffix = "Compl'Alim"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
})
</script>

<style>
.fr-pagination__list {
  @apply justify-center;
}
</style>
