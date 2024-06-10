<template>
  <AppHeader :logo-text="logoText" />
  <router-view></router-view>
  <DsfrFooter
    :logo-text="logoText"
    :cookiesLink="{ name: 'CookiesInfoPage' }"
    :legalLink="{ name: 'LegalNoticesPage' }"
    :personalDataLink="{ name: 'PrivacyPolicyPage' }"
    :afterMandatoryLinks="[{ label: 'Conditions générales d’utilisation', to: { name: 'CGUPage' } }]"
    a11yCompliance="non conforme"
    :a11yComplianceLink="{ name: 'A11yPage' }"
  >
    <template v-slot:description>
      <p>Compl'Alim</p>
    </template>
  </DsfrFooter>
</template>

<script setup>
import AppHeader from "@/components/AppHeader.vue"

const logoText = ["Ministère", "de l’Agriculture", "et de la Souveraineté", "Alimentaire"]
</script>

<style>
.fr-pagination__list {
  @apply justify-center;
}
</style>
