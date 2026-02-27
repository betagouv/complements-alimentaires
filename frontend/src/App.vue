<template>
  <div :class="lowContrastMode ? 'low-contrast-mode bg-grey-975!' : ''">
    <DsfrSkipLinks
      :links="[
        { id: 'main-content', text: 'Aller au contenu principal' },
        { id: 'navigation', text: 'Aller au menu' },
        { id: 'footer', text: 'Aller au pied de page' },
      ]"
    />

    <p v-if="environment !== 'prod'" id="env-banner" :class="`${environment} mb-0 sm:hidden`">
      Environnement de {{ environment }}
    </p>
    <AppHeader :logo-text="logoText" id="navigation" />
    <main id="main-content">
      <router-view></router-view>
    </main>
    <DsfrFooter
      :logo-text="logoText"
      :a11yComplianceLink="{ name: 'A11yPage' }"
      :cookiesLink="{ name: 'CookiesInfoPage' }"
      :legalLink="{ name: 'LegalNoticesPage' }"
      :personalDataLink="{ name: 'PrivacyPolicyPage' }"
      :afterMandatoryLinks="[
        { label: 'Conditions générales d’utilisation', to: { name: 'CGUPage' } },
        { label: 'Mesures d\'impact', to: { name: 'StatsPage' } },
        { label: 'Plan du site', to: { name: 'SiteMap' } },
      ]"
      id="footer"
      :homeLink="{ name: 'LandingPage' }"
      homeTitle="Retour à l'accueil du site Compl'Alim - Ministère de l'Agriculture, de l'Agro-alimentaire et de la Souveraineté Alimentaire"
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
const logoText = ["Ministère", "de l'Agriculture,", "de l'Agro-alimentaire", "et de la Souveraineté", "Alimentaire"]

watch(route, (to) => {
  const suffix = "Compl'Alim"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
})

const lowContrastMode = computed(() => ["IdentitySection", "HistorySection"].includes(route.name))
const environment = window.ENVIRONMENT
</script>

<style>
@reference "./styles/index.css";

.fr-pagination__list {
  @apply justify-center;
}

.low-contrast-mode {
  .border,
  .border-l {
    @apply border-gray-500;
  }
}

#env-banner {
  display: block;
  text-align: center;
  font-weight: bold;
  padding: 0.5em;
  background-color: #f60700;
}
#env-banner.dev {
  background-color: #95e257;
}
#env-banner.staging {
  background-color: #a6f2fa;
}
#env-banner.demo {
  background-color: #fcc0b0;
}
</style>
