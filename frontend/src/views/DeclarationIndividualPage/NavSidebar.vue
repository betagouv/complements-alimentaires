<template>
  <DsfrSideMenu :menuItems="menuItems" />
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

// Note:
// Il y a des hacks en attendant la résolution de https://github.com/dnum-mi/vue-dsfr/issues/1076
// Par exemple, la gestion de `expanded` ne devrait pas se faire avec le route
// Aussi, on cache l'icône (dans les styles scoped) pour ne pas faire penser aux gens
// qu'on peut collapse les sections.
const declaration = defineModel()
const route = useRoute()
const makeRoute = (name) => ({ name, params: { declarationId: declaration.value.id } })
const appendHash = (route, hash) => ({ ...{ hash }, ...route })

const productRouteName = "DeclarationIndividualPage"
const historyRouteName = "DeclarationHistoryPage"
const companyRouteName = "DeclarationCompanyPage"

const isInProduct = computed(() => route.name === productRouteName)
const isInCompany = computed(() => route.name === companyRouteName)
const isInHistory = computed(() => route.name === historyRouteName)

const productRoute = computed(() => makeRoute(productRouteName))
const companyRoute = computed(() => makeRoute(companyRouteName))
const historyRoute = computed(() => makeRoute(historyRouteName))

const menuItems = computed(() => {
  return [
    {
      to: productRoute.value,
      active: isInProduct.value,
      text: "Produit",
      expanded: isInProduct.value,
      menuItems: isInProduct.value
        ? [
            {
              to: appendHash(productRoute.value, "#resume"),
              text: "Résumé de l'instruction",
            },
            {
              to: appendHash(productRoute.value, "#vue-ensemble"),
              text: "Vue d'ensemble",
            },
            {
              to: appendHash(productRoute.value, "#composition-produit"),
              text: "Composition du produit",
            },
            {
              to: appendHash(productRoute.value, "#pieces-jointes"),
              text: "Pièces jointes",
            },
          ]
        : null,
    },
    {
      to: historyRoute.value,
      text: "Historique",
      active: isInHistory.value,
    },
    {
      to: companyRoute.value,
      text: "Fiche entreprise responsable de la mise sur le marché",
      active: isInCompany.value,
    },
  ]
})
</script>
