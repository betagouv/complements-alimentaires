<template>
  <div :class="lowContrastMode ? 'bg-grey-975!' : ''">
    <DsfrSkipLinks
      :links="[
        { id: 'main-content', text: 'Aller au contenu principal' },
        { id: 'navigation', text: 'Aller au menu' },
        { id: 'footer', text: 'Aller au pied de page' },
      ]"
    />
    <AppHeader :logo-text="logoText" id="navigation" />
    <router-view id="main-content"></router-view>
    <DsfrFooter
      :logo-text="logoText"
      :a11yComplianceLink="{ name: 'A11yPage' }"
      :cookiesLink="{ name: 'CookiesInfoPage' }"
      :legalLink="{ name: 'LegalNoticesPage' }"
      :personalDataLink="{ name: 'PrivacyPolicyPage' }"
      :afterMandatoryLinks="[
        { label: 'Conditions générales d’utilisation', to: { name: 'CGUPage' } },
        { label: 'Mesures d\'impact', to: { name: 'StatsPage' } },
      ]"
      id="footer"
    >
      <template v-slot:description>
        <p>Compl'Alim</p>
      </template>
    </DsfrFooter>
    <AppToaster :messages="messages" @close-message="removeMessage($event)" />
  </div>
</template>

<script setup>
import { watch, computed } from "vue"
import { useRoute } from "vue-router"
import AppToaster from "@/components/AppToaster.vue"
import useToaster from "@/composables/use-toaster"
import AppHeader from "@/components/AppHeader.vue"

const route = useRoute()
const { messages, removeMessage } = useToaster()
const logoText = ["Ministère", "de l’Agriculture", "et de la Souveraineté", "Alimentaire"]

watch(route, (to) => {
  const suffix = "Compl'Alim"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
})

const lowContrastMode = computed(() => route.name === "InstructionPage")
</script>

<style>
@reference "./styles/index.css";

.fr-pagination__list {
  @apply justify-center;
}
</style>
