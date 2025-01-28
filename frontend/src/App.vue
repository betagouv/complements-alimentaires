<template>
  <div :class="lowContrastMode ? 'bg-grey-975!' : ''">
    <AppHeader :logo-text="logoText" />
    <router-view></router-view>
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
@reference "../../styles/index.css";

.fr-pagination__list {
  @apply justify-center;
}
</style>
