<template>
  <DsfrSideMenu :menuItems="menuItems" />
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

const props = defineProps({ role: { type: String, default: "instruction" } })

// Note:
// Il y a des hacks en attendant la résolution de https://github.com/dnum-mi/vue-dsfr/issues/1076
// Par exemple, la gestion de `expanded` ne devrait pas se faire avec le route
// Aussi, on cache l'icône (dans les styles scoped) pour ne pas faire penser aux gens
// qu'on peut collapse les sections.
const declaration = defineModel()
const route = useRoute()
const makeRoute = (name) => ({ name, params: { declarationId: declaration.value.id } })
const appendHash = (route, hash) => ({ ...{ hash }, ...route })

const productRouteName = props.role === "instruction" ? "InstructionSection" : "VisaProductSection"
const identityRouteName = props.role === "instruction" ? "IdentitySection" : "VisaIdentitySection"
const historyRouteName = props.role === "instruction" ? "HistorySection" : "VisaHistorySection"

const isInProduct = computed(() => route.name === productRouteName)
const isInIdentity = computed(() => route.name === identityRouteName)
const isInHistory = computed(() => route.name === historyRouteName)

const productRoute = computed(() => makeRoute(productRouteName))
const identityRoute = computed(() => makeRoute(identityRouteName))
const historyRoute = computed(() => makeRoute(historyRouteName))

const menuItems = computed(() => {
  const productMenuItems = [
    {
      to: appendHash(productRoute.value, "#pieces-jointes"),
      text: "Pièces jointes",
    },
    {
      to: appendHash(productRoute.value, "#dernier-commentaire"),
      text: "Dernier commentaire",
    },
    {
      to: appendHash(productRoute.value, "#composition-produit"),
      text: "Composition du produit",
    },
    {
      to: appendHash(productRoute.value, "#notes"),
      text: "Notes pour l'administration",
    },
  ]

  const decisionSegment =
    props.role === "instruction"
      ? {
          to: appendHash(productRoute.value, "#resultat-instruction"),
          text: "Résultat de l'instruction",
        }
      : {
          to: appendHash(productRoute.value, "#resultat-visa"),
          text: "Visa / signature",
        }
  productMenuItems.splice(3, 0, decisionSegment)

  return [
    {
      to: productRoute.value,
      active: isInProduct.value,
      text: props.role === "instruction" ? "Instruction" : "Déclaration",
      expanded: isInProduct.value,
      menuItems: isInProduct.value ? productMenuItems : null,
    },
    {
      to: identityRoute.value,
      text: "Identité produit et entreprise",
      expanded: isInIdentity.value,
      active: isInIdentity.value,
      menuItems: isInIdentity.value
        ? [
            {
              to: appendHash(identityRoute.value, "#declarant-e"),
              text: "Déclarant·e",
            },
            {
              to: appendHash(identityRoute.value, "#produit"),
              text: "Informations sur le produit",
            },
            {
              to: appendHash(identityRoute.value, "#entreprise"),
              text: "Identité de l’entreprise",
            },
          ]
        : null,
    },
    {
      to: historyRoute.value,
      text: "Historique",
      active: isInHistory.value,
    },
  ]
})
</script>
